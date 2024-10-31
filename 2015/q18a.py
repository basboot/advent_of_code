import itertools
from collections import defaultdict

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *


file1 = open('q18a.txt', 'r')
lines = file1.readlines()

lights = set()

N = 100

for i, line in enumerate(lines):
    for j, char in enumerate(line.rstrip()):
        if char == "#":
            lights.add((i, j))


def n_neighbours(i, j):
    n = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == dj == 0: # skip self
                continue
            if (i + di, j + dj) in lights:
                n += 1
    return n

def corners_on():
    lights.add((0, 0))
    lights.add((0, N - 1))
    lights.add((N - 1, 0))
    lights.add((N - 1, N - 1))

for step in range(100):
    # Part 2, corners always on
    corners_on()

    next_lights = set()
    for i in range(N):
        for j in range(N):
            n = n_neighbours(i, j)
            # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise
            if (i, j) in lights and (n == 2 or n == 3):
                next_lights.add((i, j))
            # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise
            if (i, j) not in lights and n == 3:
                next_lights.add((i, j))

    lights = next_lights

corners_on()
print("Part 1/2", len(lights))


