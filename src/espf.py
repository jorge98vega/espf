# Imports

import numpy as np
from scipy.interpolate import interpn
import constants

# Functions


def center_coordinates(rqs):
    com = np.sum(rqs, axis=0)
    com = com/len(rqs)
    return rqs - com


def compute_dipole(rqs, qs, debye=True):
    p = np.dot(qs, rqs)
    if debye:
        p = p/constants.debye # eÅ to D
    return p


def dipole2charges(rp, p, q=None, d=None, debye=True):
    if q is not None and d is not None:
        raise Exception("q & d are mutually exclusive")

    if debye:
        p = p*constants.debye # D to eÅ

    if q is not None:
        q = np.abs(q)
        d = np.linalg.norm(p)/q
    if d is not None:
        d = np.abs(d)
        q = np.linalg.norm(p)/d

    up = p/np.linalg.norm(p)
    rqs = np.array([rp - 0.5*d*up, rp + 0.5*d*up])
    qs = np.array([-q, q])
    return rqs, qs


def compute_quadrupole(rqs, qs, debye=True):
    Q = np.sum(np.array([q*(3*np.outer(rq, rq) - np.linalg.norm(rq)**2*np.eye(3)) for q, rq in zip(qs, rqs)]), axis=0)
    if debye:
        Q = Q/constants.debye # eÅ^2 to DÅ
    return Q


def compute_espcharges(Rs, rs, Vs, Q=0.0):
    # https://kthpanor.github.io/echem/docs/env/esp.html
    # https://doi.org/10.1002/jcc.540050204
    def r(a, I):
        return np.linalg.norm(rs[a] - Rs[I])

    def A_element(I, J):
        return np.sum(np.array([1/r(a, I)/r(a, J) for a in range(len(rs))]))*constants.ke

    def b_component(I):
        return np.sum(np.array([Vs[a]/r(a, I) for a in range(len(rs))]))

    A = np.ones((len(Rs)+1, len(Rs)+1))
    A[-1, -1] = 0.0
    for I in range(len(Rs)):
        for J in range(len(Rs)):
            A[I, J] = A_element(I, J)

    b = np.array([b_component(I) for I in range(len(Rs))])
    b = np.append(b, Q)

    qs = np.linalg.solve(A, b)[:-1]
    return qs


def pointcharges_espf(rqs, qs, rs, volt=True):
    if np.ndim(qs) == 0:
        rqs = rqs.reshape(1, -1)
        qs = np.array([qs])

    espf = np.array([np.sum(qs/np.linalg.norm(r - rqs, axis=1)) for r in rs])
    if volt:
        espf = espf*constants.ke # e/Å to V
    return espf


def dipoles_espf(rps, ps, rs, debye=True, volt=True):
    if np.ndim(ps) == 1:
        rps = rps.reshape(1, -1)
        ps = ps.reshape(1, -1)

    if debye:
        ps = ps*constants.debye # D to eÅ
    espf = np.array([np.sum(np.sum(ps*(r - rps), axis=1)/np.linalg.norm(r - rps, axis=1)**3) for r in rs])
    if volt:
        espf = espf*constants.ke # e/Å to V
    return espf


def generate_grid(Npoints, origin, lvs):
    x = np.linspace(-lvs[0][0]/2, lvs[0][0]/2, Npoints[0])
    y = np.linspace(-lvs[1][1]/2, lvs[1][1]/2, Npoints[1])
    z = np.linspace(-lvs[2][2]/2, lvs[2][2]/2, Npoints[2])
    Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
    grid1d = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    grid3d = np.array((x, y, z))
    return grid1d, grid3d


def nearest_gridpoints_espf(grid3d, pots3d, rs, volt=True):
    dstep = grid3d[:,1] - grid3d[:,0]
    displaced = rs - grid3d[:,0]
    indices3d = np.unique(np.round(displaced/dstep).astype(int), axis=0)
    gridpoints = np.take(grid3d, indices3d)
    espf = pots3d[indices3d[:,0], indices3d[:,1], indices3d[:,2]]
    if not volt:
        espf = espf/constants.ke # V to e/Å
    return gridpoints, espf


def interpolate_espf(grid3d, pots3d, rs, volt=True, method='linear'):
    espf = interpn(grid3d, pots3d, rs, method=method)
    if not volt:
        espf = espf/constants.ke # V to e/Å
    return espf


def espf_RMSD(espf_calculator, grid3d, pots3d, rs, method='approximate'):
    if method == 'approximate':
        rs, espf = nearest_gridpoints_espf(grid3d, pots3d, rs)
    elif method == 'interpolate':
        espf = interpolate_espf(grid3d, pots3d, rs)
    RMSD = np.sqrt(np.sum((espf_calculator(rs) - espf)**2)/len(rs))
    return RMSD