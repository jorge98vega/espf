# Imports

import numpy as np

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


def read_charges(filename, Zs):
    qZ = {1: 1, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 16: 6}
    charges = []
    with open(filename) as f:
        next(f) # Ignore first line
        for line, Z in zip(f, Zs):
            data = line.split()
            charges.append(qZ[Z] - np.sum(np.array(data, dtype=float)))
    return np.array(charges)


def read_partialcharges(filename):
    symbols = []
    charges = []
    with open(filename) as f:
        next(f) # Ignore first line
        for line in f:
            data = line.split()
            symbols.append(data[0])
            charges.append(float(data[1]))
    return np.array(symbols), np.array(charges)


def read_dqs(filename):
    symbols = []
    intradqs = []
    resdqs = []
    totaldqs = []
    with open(filename) as f:
        for line in f:
            data = line.split()
            symbols.append(data[7])
            intradqs.append(-float(data[9]))
            resdqs.append(-float(data[11]))
            totaldqs.append(-float(data[13]))
    return np.array(symbols), np.array(intradqs), np.array(resdqs), np.array(totaldqs)


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


def read_ankaisdipole(filename):
    dipole = []
    with open(filename) as f:
        for line in f:
            data = line.split()
            dipole.append(-float(data[2]))
    return np.array(dipole[:3])


def read_xsf(filename):
    lvs = []
    with open(filename) as f:
        for i in range(6): next(f) # Ignore first 6 lines
        line = f.readline()
        skip = int(line.split()[0])
        for i in range(4+skip): next(f) # Ignore following 4+skip lines
        line = f.readline()
        Npoints = np.array(line.split(), dtype=int)

        line = f.readline()
        origin = np.array(line.split(), dtype=float)

        for i in range(3):
            line = f.readline()
            lvs.append(np.array(line.split(), dtype=float))

    data = np.loadtxt(filename, dtype=float, skiprows=16+skip, comments='END')
    pots1d = -data
    pots3d = -data.reshape((Npoints[2], Npoints[1], Npoints[0])).transpose()
    return Npoints, origin, np.array(lvs), pots1d, pots3d


def try_reading(read_function, filename, *args):
    try:
        output = read_function(filename, *args)
    except IOError:
        output = None
    return output