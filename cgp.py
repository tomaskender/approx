import sys
sys.path.append('./ariths-gen/')

from ariths_gen.wire_components.buses import Bus
from ariths_gen.multi_bit_circuits.approximate_multipliers import UnsignedBrokenArrayMultiplier
import numpy as np
import matplotlib.pyplot as plt

class CGP():
    def __init__(self, code, error) -> None:
        self.code = code
        self.error = error

    def run(self):
        a = Bus(N=8, prefix="a_bus")
        b = Bus(N=8, prefix="b_bus")

        # Create BAM 
        bam = UnsignedBrokenArrayMultiplier(a, b, horizontal_cut=4, vertical_cut=4)

        # Evaluate all using b'casting
        va = np.arange(256).reshape(1, -1)
        vb = va.reshape(-1, 1)
        r = bam(va, vb)

        cax = plt.imshow(np.abs(r - (va * vb)))
        plt.colorbar(cax)
        plt.title("Absolute difference")
        plt.xlabel("a")
        plt.ylabel("b")

        print("Mean average error", np.abs(r - (va * vb)).mean())
