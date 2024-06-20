import math
from itertools import permutations

import numpy as np

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

from tools.advent_tools import *

grid_no_dim, width, height = read_grid(lines, GRID_SET, f_prepare_line=lambda x: list(x.rstrip()), value_conversions={"#": True, ".": False})

assert width == 5, "width must be 5"
assert height == 5, "height must be 5"

# add dimension to grid
grid = set()

for i, j in grid_no_dim:
    grid.add((i, j, 0))


to_lower = {
    (-1, 0): (1, 2),
    (1, 0): (3, 2),
    (0, -1): (2, 1),
    (0, 1): (2, 3)
}

to_higher = {
    (-1, 0): [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    (1, 0): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    (0, -1): [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
    (0, 1): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
}

def get_neighbours(position):
    neighbours = []
    i, j, dim = position

    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        # if ni, nj is -1 or with/height add neighbour from lower dim i
        if ni == -1 or nj == -1 or ni == 5 or nj == 5:
            ni, nj = to_lower[(di, dj)]
            neighbours.append((ni, nj, dim - 1))
            continue

        # if ni, nj is 2 add neighbours from higher dimension
        if ni == 2 and nj == 2:
            for ni, nj in to_higher[(di, dj)]:
                neighbours.append((ni, nj, dim + 1))
            continue

        # add normal neighbour
        neighbours.append((ni, nj, dim))
    return neighbours



# def bio_dev(grid):
#     bio = 0
#     for i in range(height):
#         for j in range(width):
#             if (i, j) in grid:
#                 bio += 2**(i*width + j)
#     return bio



print(grid)

# print(get_neighbours((1, 1, 0)))

def show_grid(grid, dim):
    for i in range(height):
        for j in range(width):
            if (i, j, dim) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()

for _ in range(200):

    # count neighbour cells
    n_neighbours = {}
    for position in grid:
        for neighbour in get_neighbours(position):
            # add if not exists (0)
            if neighbour not in n_neighbours:
                n_neighbours[neighbour] = 0
            # count
            n_neighbours[neighbour] += 1

    # next population
    next_grid = set()
    # without neighbours nothing happens, so we only look at cells with neighbours
    for position in n_neighbours:
        # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it
        if position in grid and n_neighbours[position] == 1:
            next_grid.add(position)
        # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        if position not in grid and (n_neighbours[position] == 1 or n_neighbours[position] == 2):
            next_grid.add(position)

    grid = next_grid

print(len(grid))

