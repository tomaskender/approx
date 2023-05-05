from io import StringIO
import re
import sys
sys.path.append('./ariths-gen/')

from ariths_gen.wire_components.buses import Bus
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import numpy as np
import matplotlib.pyplot as plt
import math

# Circuit setup based on input data
ROWS=8
COLS=40
BITS_IN = 8

# CGP setup
POPULATION_SIZE = 50
MUTATIONS = 3
GENERATIONS = 30000

class CGP():
    def __init__(self, code, error) -> None:
        self.code = code
        self.error = error

    def run(self):
        # Initialize population
        population = [self.code] * POPULATION_SIZE
        
        for _ in range(GENERATIONS):
            # Find best individual
            best_fit = math.inf
            best_indiv = math.nan

            # Find best fitness
            for indiv in range(POPULATION_SIZE):
                mul = UnsignedCGPCircuit(population[indiv], [BITS_IN,BITS_IN])
                va = np.arange(2**BITS_IN)
                vb = va.reshape(-1, 1)
                r = mul(va, vb)
                baseline_r = (va * vb)
                rel_normalizer = np.clip(baseline_r, 0.01, None)

                cax = plt.imshow(np.abs(r - baseline_r))
                plt.colorbar(cax)
                plt.title("Absolute difference")
                plt.xlabel("a")
                plt.ylabel("b")
                # plt.show()

                e_mean =  np.abs(r - baseline_r).mean()
                e_max = np.abs(r - baseline_r).max()
                e_rel = np.abs((r - baseline_r)/rel_normalizer).sum()

                # Use mean error for fitness
                e = e_mean
                fit = None
                if e < self.error:
                    length = r.get_circuit_gates()
                    # TODO use depth for fitness
                    fit = e * length ** 2

                if fit and fit < best_fit:
                    best_fit = fit
                    best_indiv = indiv

            fittest = population[best_indiv]
            mutated = np.delete(population, best_indiv)

            # Perform mutations
            for i in range(len(mutated)):
                m = mutated[i]
                for _ in range(MUTATIONS):
                    pass
                mutated[i] = m

            # Create next generation
            population = [fittest] + mutated
