# Using readlines()
file1 = open('q22a.txt', 'r')
lines = file1.readlines()

import re

import numpy as np

VOID, OPEN, WALL = 0, 1, 2
TILES = {" ": VOID, ".": OPEN, "#": WALL }
DIRECTIONS = [NORTH, EAST, SOUTH, WEST] = [3, 0, 1, 2]
deltas = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}

height = 0
width = 0
for i in range(len(lines) - 2):
    height = max(height, i + 1)
    row = list(lines[i].rstrip())
    for j in range(len(row)):
        width = max(width, j + 1)

map = np.zeros((height, width))

print(width, height)

start = None

for i in range(len(lines) - 2):
    row = list(lines[i].rstrip())
    for j in range(len(row)):
        if start is None and TILES[row[j]] == OPEN:
            start = (i, j)
        map[i, j] = TILES[row[j]]


path = re.split('(\d+)', lines[len(lines) - 1].strip())
path.remove("") # remove empty strings at front...
path.remove("") # ...and end

print(map)

def get_new_position(pos, orientation):
    direction = deltas[orientation]

    next_i, next_j = pos
    next_orientation = orientation
    while True:
        next_i, next_j = next_i + direction[0], next_j + direction[1]

        # wrap around
        if next_i < 0:
            next_i = height - 1
        if next_j < 0:
            next_j = width - 1
        if next_i > height - 1:
            next_i = 0
        if next_j > width - 1:
            next_j = 0

        if map[next_i, next_j] == OPEN:
            return (next_i, next_j), next_orientation
        if map[next_i, next_j] == WALL:
            return pos, orientation
        # else keep walking through the void


pos = start
orientation = EAST

for instruction in path:
    print(instruction)
    if instruction.isnumeric():
        for i in range(int(instruction)):
            print(">", pos)
            pos, orientation = get_new_position(pos, orientation)
            print(">", pos)
    else:
        if instruction == "R":
            orientation = (orientation + 1) % len(DIRECTIONS)
        if instruction == "L":
            orientation = (orientation - 1) % len(DIRECTIONS)

print("final", pos)

# 1000 times the row, 4 times the column, and the facing.
password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + orientation

print("Part 1", password)

