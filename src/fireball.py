# Imports

import numpy as np
import read
import espf

# Classes


class FireballResults:
    def __init__(self, folder):
        self.Zs, rqs = read.read_coordinates(folder + "/input.bas")
        self.rqs = espf.center_coordinates(rqs)
        self.symbols, self.q4s = read.read_charges(folder + "/PCHARGES_IN")
        _, self.q7s = read.read_charges(folder + "/PCHARGES_OUT")
        _, self.intradips, self.resdips, self.totaldips = read.read_dipoles(folder + "/dipoles.out")
        self.Npoints, self.origin, self.lvs, self.vhartree1d, self.vhartree3d = read.read_xsf(folder + "/vhartree.xsf")
        _, _, _, self.vden1d, self.vden3d = read.read_xsf(folder + "/fftpot.xsf")
        _, _, _, self.vna1d, self.vna3d = read.read_xsf(folder + "/vna.xsf")
        self.grid1d, self.grid3d = espf.generate_grid(self.Npoints, self.origin, self.lvs)
        self.minilvs = self.lvs/(1 + np.sqrt(3))