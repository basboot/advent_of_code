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


def show_garden(reachable=0):
    for i in range(-1, height + 1):
        for j in range(-1, width + 1):
            if (i, j) in rocks:
                print("#", end="")
                if i < 0 or i > height - 1 or j < 0 or j > width - 1:  # add borders outside fiels
                    pass
                else:
                    assert bitvectors[(i, j)] & reachable == 0, "Visted a rock"
            else:
                if bitvectors[(i, j)] & reachable > 0:
                    print("O", end="")
                else:
                    print(".", end="")
        print()

# print(f"Start at {start} garder size ({height}, {width}), # tiles = {width * height} #rocks = approx. {len(rocks) - width - height}")


MAX_STEPS = 64

# 0 steps
# create bitvectors for all tiles, and populate solution with them (in zero steps you stay on same tile)
bitvectors = {}
solution = np.zeros((height + 2, width + 2), dtype=object)

for i in range(height):
    for j in range(width):
        bitvectors[(i, j)] = 1 << (i * width + j) # for easy lookup later
        if (i, j) not in rocks:  # rocks should stay unvisited
            solution[i + 1, j + 1] = 1 << (i * width + j)

# step 1 - N_STEPS
for step in range(MAX_STEPS):
    # keep old solution
    previous_solution = solution
    # start with nothing reachable
    solution = np.zeros((height + 2, width + 2), dtype=object)
    # reachable in n steps = reachable in n - 1 steps, from tiles we can reach in 1 step
    for i in range(height):
        for j in range(width):
            if (i, j) not in rocks: # rocks should stay unvisited
                # combine 4 tiles around
                solution[i + 1, j + 1] = (previous_solution[i - 1 + 1, j + 1] | previous_solution[i + 1 + 1, j + 1] |
                                           previous_solution[i + 1, j - 1 + 1] | previous_solution[i + 1, j + 1 + 1])


# only interested in what is reachable from start
reachable = solution[start[0] + 1, start[1] + 1]

total = 0
for pos in bitvectors:
    if bitvectors[pos] & reachable > 0:
        total += 1

print("Total", total)







