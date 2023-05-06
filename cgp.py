import sys
sys.path.append('./ariths-gen/')

from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import numpy as np
import matplotlib.pyplot as plt
import math
import re
from random import Random

# Circuit setup based on input data
ROWS=8
COLS=40
BITS_IN = 8

# CGP setup
POPULATION_SIZE = 100
MUTATIONS = 3
GENERATIONS = 500

CODE_RE = re.compile(r"^{(.*)}(.*)\(([^()]+)\)$")
TRIPLETS_RE = re.compile(r"\(\[(\d+)\](\d+),(\d+),(\d+)\)")
OUT_RE = re.compile(r"\d+")
class CGP():
    def __init__(self, code, error) -> None:
        self.code = code
        self.error = error

    def run(self):
        # Initialize population
        population = np.repeat(self.code, POPULATION_SIZE).astype(dtype="<U8000")
        
        for g in range(GENERATIONS):
            print("Starting generation", g+1)
            # Find best individual
            best_fit = math.inf
            best_indiv = None

            # Find best fitness
            for indiv in range(POPULATION_SIZE):
                code = population[indiv]
                mul = UnsignedCGPCircuit(code, [BITS_IN,BITS_IN])
                va = np.arange(2**BITS_IN)
                vb = va.reshape(-1, 1)
                r = mul(va, vb)
                baseline_r = (va * vb)
                rel_normalizer = np.clip(baseline_r, 0.01, None)

                # cax = plt.imshow(np.abs(r - baseline_r))
                # plt.colorbar(cax)
                # plt.title("Absolute difference")
                # plt.xlabel("a")
                # plt.ylabel("b")
                # plt.show()

                e_mean =  np.abs(r - baseline_r).mean()
                e_max = np.abs(r - baseline_r).max()
                e_rel = np.abs((r - baseline_r)/rel_normalizer).sum()

                # Use mean error for fitness
                e = e_mean
                fit = None
                if e < self.error:
                    # TODO incorporate depth into fitness
                    fit = len(mul.get_circuit_gates())

                if fit is not None and fit < best_fit:
                    best_fit = fit
                    best_indiv = indiv

            if best_indiv is not None:
                print("Best fitness is", best_fit)
                preserved = np.array([population[best_indiv]])
                mutated = np.delete(population, best_indiv)
            else:
                preserved = []
                mutated = population

            # Perform mutations
            for i in range(len(mutated)):
                m = mutated[i]
                pref, trip, out = CGP.parse_code(m)
                r = Random()
                for _ in range(r.randint(0, MUTATIONS)):
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

    @staticmethod
    def parse_code(code):
        cgp_prefix, cgp_core, cgp_outputs = CODE_RE.match(code).groups()
        cgp_triplets = TRIPLETS_RE.findall(cgp_core)
        cgp_outputs = OUT_RE.findall(cgp_outputs)
        return cgp_prefix, [list(t) for t in cgp_triplets], list(cgp_outputs)
