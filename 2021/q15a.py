# Using readlines()
import heapq
import sys
import time

from scipy.spatial.distance import cityblock

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q15a.txt', 'r')
lines = file1.readlines()

cavern, width, height = read_grid(lines, GRID_NUMPY, lambda a: a.strip(), value_conversions=None, int_conversion=True)

def get_next_actions(pos):
    actions = []

    for direction in DIRECTIONS:
        next, has_moved = next_pos(pos, direction, width, height)
        if has_moved:
            actions.append(next)

    return actions

def dijkstra(start, goal):
    explored = {start}
    to_explore = [] # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (0, start))

    while len(to_explore) > 0:
        cost, pos = heapq.heappop(to_explore)
        if pos == goal:
            print("FOUND")
            return cost

        actions = get_next_actions(pos)
        for next_pos in actions:
            if next_pos in explored: # don't explore again
                continue

            next_cost = cost + cavern[next_pos[0], next_pos[1]]

            heapq.heappush(to_explore, (next_cost, next_pos))
            explored.add(next_pos)

    return "Not found"



start = (0, 0)
goal = (height - 1, width - 1)

start_time = time.time()

print(dijkstra(start, goal))

print("--- %s seconds ---" % (time.time() - start_time))



# 1256
# 1382