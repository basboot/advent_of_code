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

original_positions = positions.copy()

# print(positions)
m, n = positions.shape # moons x dims

# start with 0 speed
velocities = np.zeros((m, n), dtype=int)

original_velocities = velocities.copy()

modulus = [0] * n

# print(m, n)

step = 0
while True:
    # print("----", (step + 1))
    for i in range(m):
        dv = np.sum(np.sign(positions - positions[i,:]), 0)
        velocities[i, :] += dv

    positions += velocities
    # print(positions)

    # TODO: check planets for original config
    not_found = False
    for j in range(n):
        if modulus[j] == 0: # only check if not found yet
            not_found = True
            if np.all(positions[:, j] == original_positions[:, j]) and np.all(velocities[:, j] == original_velocities[:, j]):
                modulus[j] = step + 1

    if not not_found:
        break
    step += 1


print(modulus)
print("Part 1", math.lcm(*modulus))