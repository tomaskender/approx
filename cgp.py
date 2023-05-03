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

        cax = plt.imshow(np.abs(r - (va * vb)))
        plt.colorbar(cax)
        plt.title("Absolute difference")
        plt.xlabel("a")
        plt.ylabel("b")
        # plt.show()

        print("Mean average error", np.abs(r - (va * vb)).mean())
