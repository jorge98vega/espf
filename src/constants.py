# Imports

import numpy as np

# Functions

def create_bondi_radii():
    # A. Bondi (1964). "van der Waals Volumes and Radii". J. Phys. Chem. 68: 441. doi:10.1021/j100785a001
    d = {}
    d["H"] = 1.2
    d["C"] = 1.7
    d["N"] = 1.55
    d["O"] = 1.52
    d["F"] = 1.47
    d["P"] = 1.8
    d["S"] = 1.8
    d["Cl"] = 1.75

    d["Ar"] = 1.88
    d["As"] = 1.85
    d["Br"] = 1.85
    d["Cd"] = 1.62
    d["Cu"] = 1.4
    d["Ga"] = 1.87
    d["Au"] = 1.66
    d["He"] = 1.4
    d["In"] = 1.93
    d["I"] = 1.98
    d["Kr"] = 2.02
    d["Pb"] = 2.02
    d["Li"] = 1.82
    d["Mg"] = 1.73
    d["Hg"] = 1.70
    d["Ne"] = 1.54
    d["Ni"] = 1.64
    d["Pd"] = 1.63
    d["Pt"] = 1.8
    d["K"] = 2.75
    d["Se"] = 1.90
    d["Si"] = 2.1
    d["Ag"] = 1.9
    d["Na"] = 2.27
    d["Te"] = 2.06
    d["Tl"] = 1.96
    d["Sn"] = 2.17
    d["U"] = 1.86
    d["Xe"] = 2.16
    d["Zn"] = 1.37
    return d


# Constants

BONDI_RADII = create_bondi_radii()
# https://en.wikipedia.org/wiki/Debye
debye = 0.2081943 # eÅ
# https://en.wikipedia.org/wiki/Vacuum_permittivity
eps0 = 55.26349406e-4 # e/V/Å
ke = 1/(4*np.pi*eps0) # VÅ/e