import math
from functools import cache
from itertools import permutations

import numpy as np
import heapq

file1 = open('q18a.txt', 'r')
lines = file1.readlines()

from tools.advent_tools import *

walls = set() # (i, j)
keys = {} # (i, j): a
doors = {} # (i, j): A
start = None

for i in range(len(lines)):
    row = list(lines[i].rstrip())
    for j in range(len(row)):
        match row[j]:
            case ".":
                pass # ignore empty
            case "@":
                start = (i, j)
            case "#":
                walls.add((i, j))
            case _ if row[j].islower():
                keys[(i, j)] = row[j]
            case _ if row[j].isupper():
                doors[(i, j)] = row[j]
            case _:
                assert True, "This should not be possible"
# print(doors)

# TODO: choose strategy: random walk, or walk from key to key? => seems strange to ignore knowledge, so use keys
# TODO: remove doors and invalidate paths which go through a door? (may be suboptimal?)

@cache
# bfs / astar to find path to key
def steps_to_position(start, goal, doors):
    open_list = []
    explored = set()

    heapq.heappush(open_list, (0, start, (0, 0)))  # (f, state, parent)

    while open_list:
        _, current_position, parent = heapq.heappop(open_list)

        if current_position == goal:
            return parent[1]

        explored.add(current_position)

        for next_position, cost in successors_4_directions(current_position):
            if next_position in explored:
                continue
            if next_position in walls: # cannot walk through walls
                continue
            if next_position in doors:
                continue

            g = parent[0] + cost
            h = heuristic(next_position, goal)
            f = g + h

            heapq.heappush(open_list, (f, next_position, (g, parent[1] + 1)))

    return None  # No path found

def heuristic(state, goal_state):
    # TODO: replace with manhattan if not fast enough
    x1, y1 = state
    x2, y2 = goal_state
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Example successors function for 2D grid (moving in 4 directions)
def successors_4_directions(state):
    i, j = state
    successors = []
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_i, next_j = i + di, j + dj
        successors.append(((next_i, next_j), 1))  # Cost of moving to the next state is 1
    return successors


min_steps = math.inf

# TODO: replace with dijkstra
# dfs to find all keys
def find_keys(start, keys, doors, steps, keys_found = []):
    global min_steps
    if len(keys) == 0:
        # print(f"Found all keys in {steps} steps, {keys_found}")
        min_steps = min(min_steps, steps)

    for key in keys:
        next_steps = steps_to_position(start, key, tuple(doors.keys()))
        # print("Try", keys[key])
        if next_steps is not None:

            # print(doors, keys, keys[key].upper())
            door = keys[key].upper()
            next_doors = {key:val for key, val in doors.items() if val != door}
            next_keys = keys.copy()
            del next_keys[key]
            find_keys(key, next_keys, next_doors, next_steps + steps, keys_found + [keys[key]])



find_keys(start, keys, doors, 0)


print("Part 1", min_steps)






