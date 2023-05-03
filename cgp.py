import sys
sys.path.append('./ariths-gen/')

from ariths_gen.wire_components.buses import Bus
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import numpy as np
import matplotlib.pyplot as plt

N = 8

class CGP():
    def __init__(self, code, error) -> None:
        self.code = code
        self.error = error

    def run(self):
        # Create MUL 
        mul = UnsignedCGPCircuit(self.code, [N,N])

        # Evaluate all using b'casting
        va = np.arange(2**N)
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

        print("Mean average error", np.abs(r - baseline_r).mean())
        print("Max error", np.abs(r - baseline_r).max())
        print("Relative error", np.abs((r - baseline_r)/rel_normalizer).sum())
