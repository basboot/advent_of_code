# Using readlines()
import sys

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

trees, width, height = read_grid(lines, GRID_SET, lambda a: a.strip(), {".": None, "<": None, ">": None, "^": None, "v": None, "#": True}, )
map, width, height = read_grid(lines, GRID_DICT, lambda a: a.strip(),  )

# add trees to close the map
start = (0, 1)
trees.add((-1, 1)) # start
goal = (height - 1, width - 2)
trees.add((height, width - 2)) # goal

ACTION_MAP = {
    ".": [NORTH, EAST, SOUTH, WEST],
    "<": [WEST],
    ">": [EAST],
    "^": [NORTH],
    "v": [SOUTH],
    "#": [] # should not be possible to land on a tree
}


# longest path problem is NP-hard, so we need to brute force

def dfs(pos, visited: set) -> int:
    visited.add(pos)

    if pos == goal:
        return len(visited) - 1 # return steps, not visits so -1

    max_len = 0
    for action in ACTION_MAP[map[pos]]:
        next, _ = next_pos(pos, action)
        if next in visited or next in trees: # never visit same tile twice, and don't visit trees
            continue
        next_len = dfs(next, visited.copy())
        max_len = max(max_len, next_len)
    return max_len

print(dfs(start, set()))





