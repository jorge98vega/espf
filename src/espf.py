# Imports

import numpy as np
import constants

# Functions

def compute_dipole(rqs, qs, Debye=True):
    p = np.dot(qs, rqs)
    if Debye:
        p = p/constants.Debye # eÅ to D
    return p


def pointcharges_espf(rqs, qs, rs):
    espf = [np.sum(qs/np.linalg.norm(r - rqs, axis=1)) for r in rs]
    return np.array(espf)


def dipoles_espf(rps, ps, rs, Debye=True):
    if Debye:
        ps = ps*constants.Debye # D to eÅ
    espf = [np.sum(np.sum(ps*(r - rps), axis=1)/np.linalg.norm(r - rps, axis=1)**3) for r in rs]
    return np.array(espf)