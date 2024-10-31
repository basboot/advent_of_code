import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

grid = set() # keeps only locations (as complex number) of infected nodes

for i in range(len(lines)):
    line = lines[i].rstrip()
    for j in range(len(line)):
        if line[j] == "#":
            grid.add(i + j*1j)

middle = len(lines) // 2

current_node = middle + middle * 1j
direction = -1

print(current_node)

print(direction) # turn left *1j, turn right *-1j

infected = 0

for _ in range(10000):
    # infected? turn right, not infected turn left
    if current_node in grid:
        direction *= -1j
        grid.remove(current_node)
    else:
        direction *= 1j
        grid.add(current_node)
        infected += 1
    current_node += direction

print(len(grid), infected)
