import sys
sys.path.append('./ariths-gen/')

from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import itertools
import math
import numpy as np
import re
from random import Random

# Circuit setup based on input data
ROWS=8
COLS=40
BITS_IN = 8

# CGP setup
POPULATION_SIZE = 500
MUTATIONS_BASE = 3
MUTATIONS_BONUS = 2
IMPROVEMENT_WATCHDOG = 4

CODE_RE = re.compile(r"^{(.*)}(.*)\(([^()]+)\)$")
TRIPLETS_RE = re.compile(r"\(\[(\d+)\](\d+),(\d+),(\d+)\)")
OUT_RE = re.compile(r"\d+")
class CGP():
    def __init__(self, code: str, error: float) -> None:
        self.code = code
        self.error = error

    def run(self):
        # Initialize population
        population = np.repeat(self.code, POPULATION_SIZE).astype(dtype="<U8000")
        
        gens_since_improvement = 0
        prev_fit = math.inf
        for g in itertools.count(start=0, step=1):
            print("Starting generation", g+1)
            # Find best individual
            best_fit = math.inf
            best_error = math.inf
            best_indiv = None

            # Find best fitness
            for indiv in range(POPULATION_SIZE):
                code = population[indiv]
                mul = UnsignedCGPCircuit(code, [BITS_IN,BITS_IN])
                va = np.arange(2**BITS_IN)
                vb = va.reshape(-1, 1)
                r = mul(va, vb)
                baseline_r = (va * vb)
                #rel_normalizer = np.clip(baseline_r, 0.01, None)

                e_mean =  np.abs(r - baseline_r).mean() / (2 ** (2*BITS_IN))
                #e_max = np.abs(r - baseline_r).max()
                #e_rel = np.abs((r - baseline_r)/rel_normalizer).sum()

                # Use mean error for fitness normalized by number of calculations
                e = e_mean
                fit = None
                if e < self.error:
                    # TODO incorporate depth into fitness
                    fit = len(mul.get_circuit_gates())

                if fit is not None and fit < best_fit:
                    best_fit = fit
                    best_error = e
                    best_indiv = indiv

            if best_indiv is not None:
                print("Best fitness is", best_fit)
                preserved = np.array([population[best_indiv]])
                mutated = np.repeat(self.code, POPULATION_SIZE-1)
            else:
                preserved = np.array([])
                mutated = np.repeat(self.code, POPULATION_SIZE)

            # Watchdog that kills generation once best solution converges
            if best_fit < prev_fit:
                gens_since_improvement = 0
            else:
                gens_since_improvement += 1
                if gens_since_improvement >= IMPROVEMENT_WATCHDOG:
                    # best solution has already converged
                    # break off generation of future generations
                    break
            prev_fit = best_fit

            # Perform mutations
            for i in range(len(mutated)):
                m = mutated[i]
                pref, trip, out = CGP.parse_code(m)
                r = Random()
                mut_cnt = int(MUTATIONS_BASE + g * MUTATIONS_BONUS)
                for _ in range(r.randint(int(mut_cnt/2), mut_cnt)):
                    # Pick gate
                    gate = r.randint(0, ROWS*COLS-1)
                    # Mutate gate
                    trip[gate][3] = r.randint(8, 9) # 8 is constant 1, 9 is constant 0
                triplets = "".join([("([" + str(t[0]) + "]" + ",".join(map(str,t[1:])) + ")") for t in trip])
                out = ",".join(map(str,out))
                m = f"{{{pref}}}{triplets}({out})"
                mutated[i] = m

            # Create next generation
            population = np.append(preserved, mutated)
        print("Best found code is:\n{}\nwith error {:.2f} and fitness {}" % (preserved, best_error, best_fit))

    @staticmethod
    def parse_code(code):
        cgp_prefix, cgp_core, cgp_outputs = CODE_RE.match(code).groups()
        cgp_triplets = TRIPLETS_RE.findall(cgp_core)
        cgp_outputs = OUT_RE.findall(cgp_outputs)
        return cgp_prefix, [list(t) for t in cgp_triplets], list(cgp_outputs)
