import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q11a.txt', 'r')
path = file1.readlines()[0].rstrip().split(",")


print(path)

def distance(position):
    return (abs(position[0]) - abs(position[1])) + abs(position[1] / 0.5)


directions = {
    "n": np.array([-1, 0]),
    "ne": np.array([-0.5, 0.5]),
    "se": np.array([0.5, 0.5]),
    "s": np.array([1, 0]),
    "sw": np.array([0.5, -0.5]),
    "nw": np.array([-0.5, -0.5]),
}

position = np.array([0.0, 0.0])
max_distance = -math.inf

for step in path:
    position += directions[step]
    max_distance = max(max_distance, distance(position))

print("Child position", position)

print("Part 1", distance(position))
print("Part 2", max_distance)