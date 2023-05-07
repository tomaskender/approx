import sys
sys.path.append('./ariths-gen/')

from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import itertools
import math
import numpy as np
import re
from random import Random

# Circuit setup based on input data
BITS_IN = 8

# CGP setup
POPULATION_SIZE = 300
MUTATIONS_BASE = 3
MUTATIONS_BONUS = 2
IMPROVEMENT_WATCHDOG = 4

CODE_RE = re.compile(r"^{(.*)}(.*)\(([^()]+)\)$")
TRIPLETS_RE = re.compile(r"\(\[(\d+)\](\d+),(\d+),(\d+)\)")
OUT_RE = re.compile(r"\d+")
class CGP():
    def __init__(self, code: str, error: float) -> None:
        self.code = code
        self.gates_count = len(UnsignedCGPCircuit(code, [BITS_IN,BITS_IN]).get_circuit_gates())
        self.error = error

    def run(self):
        # Initialize population
        population = np.repeat(self.code, POPULATION_SIZE).astype(dtype="<U8000")
        
        normalizer = 2 ** (2*BITS_IN)
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

                e_mean =  np.abs(r - baseline_r).mean() / normalizer
                fit = None
                if e_mean < self.error:
                    # TODO incorporate depth into fitness
                    fit = len(mul.get_circuit_gates())

                if fit is not None and fit < best_fit:
                    best_fit = fit
                    best_error = e_mean

                    rel_normalizer = np.clip(baseline_r, 1, None)
                    best_error_max = np.abs(r - baseline_r).max()
                    best_error_rel = np.abs((r - baseline_r)/rel_normalizer).mean()
                    best_indiv = indiv

            if best_indiv is not None:
                print("Current gate count is", best_fit)
                print("Errors: [mean] {:.3f}, [max] {:d}, [rel mean] {:.3f}".format(best_error, best_error_max, best_error_rel))
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
                    print("Best found code is:")
                    print(preserved)
                    print("with mean error {:.3f}% and fitness {}.".format(100*best_error, best_fit))
                    print("Circuit has been reduced to {:.1f}% of original circuit.".format(100*best_fit/self.gates_count))
                    exit(0)
            prev_fit = best_fit

            # Perform mutations
            for i in range(len(mutated)):
                m = mutated[i]
                pref, trip, out = CGP.parse_code(m)
                r = Random()
                mut_cnt = int(MUTATIONS_BASE + g * MUTATIONS_BONUS)
                for _ in range(r.randint(int(mut_cnt/2), mut_cnt)):
                    # Pick gate
                    gate = r.randint(0, self.gates_count-1)
                    # Mutate gate
                    trip[gate][3] = r.randint(8, 9) # 8 is constant 1, 9 is constant 0
                triplets = "".join([("([" + str(t[0]) + "]" + ",".join(map(str,t[1:])) + ")") for t in trip])
                out = ",".join(map(str,out))
                m = f"{{{pref}}}{triplets}({out})"
                mutated[i] = m

            # Create next generation
            population = np.append(preserved, mutated)

    @staticmethod
    def parse_code(code):
        cgp_prefix, cgp_core, cgp_outputs = CODE_RE.match(code).groups()
        cgp_triplets = TRIPLETS_RE.findall(cgp_core)
        cgp_outputs = OUT_RE.findall(cgp_outputs)
        return cgp_prefix, [list(t) for t in cgp_triplets], list(cgp_outputs)
