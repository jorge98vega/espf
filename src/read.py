# Imports

import numpy as np
import time

# Functions

def read_coordinates(filename):
    Zs = []
    positions = []
    with open(filename) as f:
        next(f) # Ignore first line
        for line in f:
            data = line.split()
            Zs.append(int(data[0]))
            positions.append(np.array(data[1:], dtype=float))
    return np.array(Zs), np.array(positions)


def read_charges(filename):
    symbols = []
    charges = []
    with open(filename) as f:
        next(f) # Ignore first line
        for line in f:
            data = line.split()
            symbols.append(data[0])
            charges.append(float(data[1]))
    return np.array(symbols), np.array(charges)


def read_dipoles(filename):
    symbols = []
    intradips = []
    resdips = []
    totaldips = []
    with open(filename) as f:
        for line in f:
            data = line.split()
            symbols.append(data[7])
            intradips.append(-np.array(data[9:12], dtype=float))
            resdips.append(-np.array(data[13:16], dtype=float))
            totaldips.append(-np.array(data[17:], dtype=float))
    return np.array(symbols), np.array(intradips), np.array(resdips), np.array(totaldips)


def read_xsf(filename):
    lvs = []
    with open(filename) as f:
        for i in range(14): next(f) # Ignore first 14 lines
        line = f.readline()
        Npoints = np.array(line.split(), dtype=int)

        line = f.readline()
        origin = np.array(line.split(), dtype=float)
        
        for i in range(3):
            line = f.readline()
            lvs.append(np.array(line.split(), dtype=float))

    data = np.genfromtxt(filename, dtype=float, skip_header=19, skip_footer=2)
    pots1d = -data
    pots3d = -data.reshape((Npoints[2], Npoints[1], Npoints[0])).transpose()
    return Npoints, origin, np.array(lvs), pots1d, pots3d