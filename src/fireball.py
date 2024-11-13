# Imports

import numpy as np
import read
import espf

# Classes


class FireballResults:
    def __init__(self, folder):
        self.Zs, self.bas = read.read_coordinates(folder + "/input.bas")
        self.rqs = espf.center_coordinates(self.bas)
        self.symbols, _ = read.read_partialcharges(folder + "/PCHARGES_IN")
        qs = {}
        for i in range(1, 8):
            qs[i] = read.read_charges(folder + "/CHARGES_" + str(i), self.Zs)
        self.qs = qs
        _, self.intradips, self.resdips, self.totaldips = read.read_dipoles(folder + "/dipoles.out")
        self.Npoints, self.origin, self.lvs, self.vhartree1d, self.vhartree3d = read.read_xsf(folder + "/vhartree.xsf")
        _, _, _, self.vden1d, self.vden3d = read.read_xsf(folder + "/fftpot.xsf")
        _, _, _, self.vna1d, self.vna3d = read.read_xsf(folder + "/vna.xsf")
        self.grid1d, self.grid3d = espf.generate_grid(self.Npoints, self.origin, self.lvs)
        self.minilvs = self.lvs/(1 + np.sqrt(3))

    def compute_espcharges(self, rs):
        espf_vhartree = espf.interpolate_espf(self.grid3d, self.vhartree3d, rs)
        self.qs["esp"] = espf.compute_espcharges(self.rqs, rs, espf_vhartree)