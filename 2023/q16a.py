# Using readlines()
import sys
import time
from functools import cache

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

BOUNCE = {
    ".": {
        NORTH: [NORTH], EAST: [EAST], SOUTH: [SOUTH], WEST: [WEST]
    },
    "\\": {
        NORTH: [WEST], EAST: [SOUTH], SOUTH: [EAST], WEST: [NORTH]
    },
    "/": {
        NORTH: [EAST], EAST: [NORTH], SOUTH: [WEST], WEST: [SOUTH]
    },
    "-": {
        NORTH: [EAST, WEST], EAST: [EAST], SOUTH: [EAST, WEST], WEST: [WEST]
    },
    "|": {
        NORTH: [NORTH], EAST: [NORTH, SOUTH], SOUTH: [SOUTH], WEST: [NORTH, SOUTH]
    },
}


cave, width, height = read_grid(lines, GRID_DICT, lambda a: list(a.strip()))

# print(cave)

# assert cave[(0, 0)] == ".", "Entry point not empty"
start = (0, 0, EAST) # TODO: check orient ant rotate if needed


def next_orientations(pos):
    i, j, orientatation = pos

    return [(i, j, direction) for direction in BOUNCE[cave[(i, j)]][orientatation]]

def dfs_old(current_pos, visited):
    if current_pos in visited:
        pass # TODO: check

    i, j, orientation = current_pos
    (next_i, next_j), has_moved = next_pos((i, j), orientation, width, height)

    if has_moved:
        for next_pos_and_orientation in next_orientations((next_i, next_j, orientation)):
            if next_pos_and_orientation not in visited:
                visited.add(next_pos_and_orientation)
                visited = dfs(next_pos_and_orientation, visited)
        return visited
    else:
        # no move possible
        return visited



def dfs(current_pos, visited):

    if current_pos in visited:
        return visited
    # add curent
    visited.add(current_pos)
    # first check orientations
    next_positions = next_orientations(current_pos)

    for next_position in next_positions:
        i, j, orientation = next_position
        (next_i, next_j), has_moved = next_pos((i, j), orientation, width, height)
        if has_moved:
            visited.union(dfs((next_i, next_j, orientation), visited))

    return visited



start_time = time.time()

max_tiles = -math.inf

def count_energized(pos):
    visited = set()
    # visited.add(start)
    visited = dfs(pos, visited)
    positions = set()
    for pos in visited:
        positions.add(pos[0:2])

    return len(positions)

pos = start

for i in range(height):
    print("i", i)
    pos = (i, 0, EAST)
    max_tiles = max(count_energized(pos), max_tiles)
    pos = (i, width - 1, WEST)
    max_tiles = max(count_energized(pos), max_tiles)

for j in range(width):
    print("j", j)
    pos = (0, j, SOUTH)
    max_tiles = max(count_energized(pos), max_tiles)
    pos = (height - 1, j, NORTH)
    max_tiles = max(count_energized(pos), max_tiles)

print(max_tiles)

print("--- %s seconds ---" % (time.time() - start_time))

# 6268 too low

# 229 sec = v1
