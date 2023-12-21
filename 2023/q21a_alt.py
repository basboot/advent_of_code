# Using readlines()
from tools.advent_tools import *
import numpy as np

file1 = open('q21a.txt', 'r')
lines = file1.readlines()

height = len(lines)
width = len(lines[0].rstrip())
rocks = set()
for i in range(-1, height + 1):
    for j in range(-1, width + 1):
        if i < 0 or i > height - 1 or j < 0 or j > width - 1: # add borders outside fiels
            rocks.add((i, j))
            continue

        # print(height, width, i, j)
        if lines[i].rstrip()[j] == "S":
            start = (i, j)
        if lines[i].rstrip()[j] == "#":
            rocks.add((i, j))


reachable = {}

def get_next_positions(pos):
    i, j = pos
    next_positions = []
    for ni, nj in [(i + di, j + dj) for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
        if (ni, nj) not in rocks:
            next_positions.append((ni, nj))
    return next_positions

MAX_STEPS = 6

next_positions = [start]
reachable[start] = 0 # modulus 2
for step in range(MAX_STEPS):
    positions = next_positions
    next_positions = []
    while len(positions) > 0:
        pos = positions.pop() # order does not matter

        for pos in get_next_positions(pos):
            if pos in reachable:
                continue # don't visit again
            else:
                next_positions.append(pos)
                reachable[pos] = step + 1 # admin when reachable, and don't visit again

total = 0
for pos in reachable:
    if (MAX_STEPS - reachable[pos]) % 2 == 0:
        total += 1
print("Total", total)









