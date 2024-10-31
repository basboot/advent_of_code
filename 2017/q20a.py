import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

positions = []
velocities = []
accelerations = []

for line in lines:
    p, v, a =[[int(x) for x in c.split(",")] for c in line.rstrip().replace("<","").replace(">","").replace("p=","").replace("v=","").replace("a=","").split(", ")]
    positions.append(p)
    velocities.append(v)
    accelerations.append(a)

positions = np.array(positions)
velocities = np.array(velocities)
accelerations = np.array(accelerations)

# print(positions)

# Part 1
# while True:
#     # update velocity
#     velocities += accelerations
#     # update positions
#     positions += velocities
#     # check closest
#     # print(np.sum(np.abs(positions), axis=1))
#     print(np.argmin(np.sum(np.abs(positions), axis=1)))
#     print("--")

# Part 2
while True:
    # update velocity
    velocities += accelerations
    # update positions
    positions += velocities

    # only keep particles without collision
    positions, surviving_rows, row_counts = np.unique(positions, axis=0, return_index=True, return_counts=True)

    # step one: remove not unique
    velocities = velocities[surviving_rows, :]
    accelerations = accelerations[surviving_rows, :]

    # step two: remove unique with rowcount > 1
    positions = positions[row_counts == 1]
    velocities = velocities[row_counts == 1]
    accelerations = accelerations[row_counts == 1]

    print(len(velocities))
