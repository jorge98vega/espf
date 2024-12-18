# Imports

import numpy as np
import read
import espf

# Classes


class FireballResults:
    def __init__(self, folder):
        self.Zs, self.bas = read.read_coordinates(folder + "/input.bas")
        self.rqs = espf.center_coordinates(self.bas)
        qs = {}
        for i in [1, 2, 3, 4, 7]:
            qs[i] = read.read_charges(folder + "/CHARGES_" + str(i), self.Zs)
        self.qs = qs
        self.ankaisdip = read.try_reading(read.read_ankaisdipole, folder + "/Ankais.out")
        self.symbols, self.intradips, self.resdips, self.totaldips = read.read_dipoles(folder + "/dipoles.out")
        _, self.intradqs, self.resdqs, self.totaldqs = read.try_reading(read.read_dqs, folder + "/dq_DPs.out") or (None, None, None, None)
        self.Npoints, self.origin, self.lvs, self.vhartree1d, self.vhartree3d = read.read_xsf(folder + "/vhartree.xsf")
        _, _, _, self.vden1d, self.vden3d = read.read_xsf(folder + "/fftpot.xsf")
        _, _, _, self.vna1d, self.vna3d = read.read_xsf(folder + "/vna.xsf")
        self.minilvs = self.lvs/(1 + np.sqrt(3))
        self.grid1d, self.grid3d = espf.generate_grid(self.Npoints, self.origin, self.lvs)

    def compute_espcharges(self, rs, method='approximate'):
        if method == 'approximate':
            rs, espf_vhartree = espf.nearest_gridpoints_espf(self.grid3d, self.vhartree3d, rs)
        elif method == 'interpolate':
            espf_vhartree = espf.interpolate_espf(self.grid3d, self.vhartree3d, rs)
        self.qs["esp"] = espf.compute_espcharges(self.rqs, rs, espf_vhartree)

    def check_points(self, rs):
        xlim, ylim, zlim = np.diag(self.minilvs/2)
        inside_minicell = np.all((-xlim <= rs[:, 0]) & (rs[:, 0] <= xlim) &
                                 (-ylim <= rs[:, 1]) & (rs[:, 1] <= ylim) &
                                 (-zlim <= rs[:, 2]) & (rs[:, 2] <= zlim))
        if not inside_minicell:
            print("WARNING! Some points are outside the minicell")