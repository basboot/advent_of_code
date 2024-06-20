import math
from itertools import permutations

import numpy as np

file1 = open('q12a.txt', 'r')
lines = file1.readlines()

positions = []
for line in lines:
    row = [int(x) for x in line.rstrip().replace("<x=","").replace(" y=", "").replace(" z=", "").replace(">", "").split(",")]
    positions.append(row)

positions = np.array(positions)

# print(positions)
m, n = positions.shape # moons x dims

# start with 0 speed
velocities = np.zeros((m, n), dtype=int)

# print(m, n)

for step in range(1000):
    # print("----", (step + 1))
    for i in range(m):
        dv = np.sum(np.sign(positions - positions[i,:]), 0)
        velocities[i, :] += dv

    positions += velocities
    # print(positions)

pot_energy = np.sum(np.abs(positions), 1)
kin_energy = np.sum(np.abs(velocities), 1)

energy = np.sum(pot_energy * kin_energy)

print(energy)