# Imports

import numpy as np


# Functions


def create_bondi_radii():
    # A. Bondi (1964). "van der Waals Volumes and Radii". J. Phys. Chem. 68: 441. doi:10.1021/j100785a001
    r = {} # Å
    r["H"] = 1.2
    r["C"] = 1.7
    r["N"] = 1.55
    r["O"] = 1.52
    r["F"] = 1.47
    r["P"] = 1.8
    r["S"] = 1.8
    r["Cl"] = 1.75

    r["Ar"] = 1.88
    r["As"] = 1.85
    r["Br"] = 1.85
    r["Cd"] = 1.62
    r["Cu"] = 1.4
    r["Ga"] = 1.87
    r["Au"] = 1.66
    r["He"] = 1.4
    r["In"] = 1.93
    r["I"] = 1.98
    r["Kr"] = 2.02
    r["Pb"] = 2.02
    r["Li"] = 1.82
    r["Mg"] = 1.73
    r["Hg"] = 1.70
    r["Ne"] = 1.54
    r["Ni"] = 1.64
    r["Pd"] = 1.63
    r["Pt"] = 1.8
    r["K"] = 2.75
    r["Se"] = 1.90
    r["Si"] = 2.1
    r["Ag"] = 1.9
    r["Na"] = 2.27
    r["Te"] = 2.06
    r["Tl"] = 1.96
    r["Sn"] = 2.17
    r["U"] = 1.86
    r["Xe"] = 2.16
    r["Zn"] = 1.37

    r["B"] = 1.92 # https://doi.org/10.1021/jp8111556
    return r


# Constants

BONDI_RADII = create_bondi_radii() # Å
# https://en.wikipedia.org/wiki/Debye
debye = 0.2081943 # eÅ
# https://en.wikipedia.org/wiki/Vacuum_permittivity
eps0 = 55.26349406e-4 # e/V/Å
ke = 1/(4*np.pi*eps0) # VÅ/e