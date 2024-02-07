# Imports

import numpy as np
import constants

# Functions

def dotsphere(radius, density):
    # M. Deserno (2004). "How to generate equidistributed points on the surface of a sphere". https://www.cmu.edu/biolphys/deserno/pdf/sphere_equi.pdf
    Ncount = 0
    a = 1/density/radius**2
    d = np.sqrt(a)
    Mtheta = round(np.pi/d)
    dtheta = np.pi/Mtheta
    dphi = a/dtheta

    points = []
    for m in range(Mtheta):
        theta = np.pi*(m + 0.5)/Mtheta
        Mphi = round(2*np.pi*np.sin(theta)/dphi)
        for n in range(Mphi):
            phi = 2*np.pi*n/Mphi
            points.append(np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]))
            Ncount += 1
    return np.array(points)*radius


def vdw_surface(coordinates, elements, scale_factor=1.0, density=1.0):
    # https://github.com/rmcgibbo/pyvdwsurface
    # Compute points on the VDW surface of a molecule
    
    # Parameters
    # ----------
    # coordinates : np.ndarray, shape=(n_atoms, 3)
    #     The cartesian coordinates of the nuclei, in units of ANGSTROMS
    # elements : list, shape=(n_atoms)
    #     The element symbols (C, H, etc) for each of the nuceli
    # scale_factor : float
    #     The points on the molecular surface are set at a distance of
    #     scale_factor * vdw_radius away from each of the atoms.
    # density : float
    #     The (approximate) number of points to generate per square angstrom
    #     of surface area. 1.0 is the default recommended by Kollman & Singh.
    if len(coordinates) != len(elements):
        print("coordinate.size does not match elements.size")
        return

    radii = {}
    for element in elements:
        if element in constants.BONDI_RADII:
            if element not in radii:
                radii[element] = constants.BONDI_RADII[element] * scale_factor
        else:
            print("%s is not a supported element", element)
            return

    surfacepoints = []
    surfacemesh = []

    for element in radii.keys():
        dots = dotsphere(radii[element], density)

        for i, ei in enumerate(elements):
            if ei != element:
                continue
            dotsi = coordinates[i] + dots

            neighbors = [] # all of the atoms that i is close to
            for j, ej in enumerate(elements):
                if i == j:
                    continue
                d = np.linalg.norm(coordinates[i] - coordinates[j])
                if d < (radii[ei] + radii[ej]):
                    neighbors.append((d, j, ej))
    
            for dot in dotsi:
                accessible = True
                for neighbor in neighbors:
                    if np.linalg.norm(coordinates[neighbor[1]] - dot) < radii[neighbor[2]]:
                        accessible = False
                        break
                if accessible:
                    surfacepoints.append(dot)

    return np.array(surfacepoints), surfacemesh