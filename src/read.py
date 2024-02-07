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
            positions.append(np.array([float(datum) for datum in data[1:]]))
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
            intradips.append(np.array([float(datum) for datum in data[9:12]]))
            resdips.append(np.array([float(datum) for datum in data[13:16]]))
            totaldips.append(np.array([float(datum) for datum in data[17:]]))
    return np.array(symbols), -np.array(intradips), -np.array(resdips), -np.array(totaldips)