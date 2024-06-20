import math
from itertools import permutations

import numpy as np

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

from tools.advent_tools import *

grid, width, height = read_grid(lines, GRID_SET, f_prepare_line=lambda x: list(x.rstrip()), value_conversions={"#": True, ".": False})


def count_neighbours(position, grid):
    neighbours = 0
    i, j = position
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (i + di, j + dj) in grid:
            neighbours += 1
    return neighbours

def show_grid(grid):
    for i in range(height):
        for j in range(width):
            if (i, j) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()

def bio_dev(grid):
    bio = 0
    for i in range(height):
        for j in range(width):
            if (i, j) in grid:
                bio += 2**(i*width + j)
    return bio

def grid_to_tuple(grid):
    tiles = list(grid)
    tiles.sort()
    return tuple(tiles)

history = {grid_to_tuple(grid)}

print(history)

while True:
    next_grid = set()
    # show_grid(grid)
    for i in range(height):
        for j in range(width):
            neighbours = count_neighbours((i, j), grid)
            if (i, j) in grid:
                if neighbours == 1:
                    next_grid.add((i, j))
            else:
                if neighbours == 1 or neighbours == 2:
                    next_grid.add((i, j))
    hist_grid = grid_to_tuple(next_grid)
    if hist_grid in history:
        print("FOUND")
        break

    history.add(hist_grid)
    grid = next_grid

print()
show_grid(next_grid)

print("Part 1", bio_dev(next_grid))



