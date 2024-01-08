# Using readlines()
import heapq
import sys
import time

from scipy.spatial.distance import cityblock

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q17a.txt', 'r')
lines = file1.readlines()

city, width, height = read_grid(lines, GRID_NUMPY, lambda a: a.strip(), value_conversions=None, int_conversion=True)


MAX_STRAIGHT = 10 #Part 1, 3
MIN_STRAIGHT = 4 #Part 1, 0

# prepare movements

DIRECTIONS = {
    NORTH: [(-1, 0), (-2, 0), (-3, 0)],
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}


def get_next_actions(pos, orientation, n_straight):
    actions = []
    # 90 degrees not always an option
    directions = []
    if n_straight >= MIN_STRAIGHT:
        directions.append((orientation + 1) % len(DIRECTIONS))
        directions.append((orientation + 3) % len(DIRECTIONS))
    # straight not always an option
    if n_straight < MAX_STRAIGHT:
        directions.append(orientation)

    for direction in directions:
        next, has_moved = next_pos(pos, direction, width, height)
        if has_moved:
            actions.append(((next), direction, n_straight + 1 if direction == orientation else 1))

    return actions

def heuristic_knightmoves(pos, goal):
    dx = abs(pos[0] - goal[0])
    dy = abs(pos[1] - goal[1])

    longest = max(dx, dy)
    shortest = min(dx, dy)

    est_longest_large_steps = (longest // 3)
    est_longest_small_steps = (longest % 3)

    if est_longest_large_steps >= shortest:
        est_smallest_large_steps = 0
        est_smallest_small_steps = (est_longest_large_steps - shortest) % 2
    else:
        remaning = shortest - est_longest_large_steps

        est_smallest_large_steps = (remaning // 3)
        est_smallest_small_steps = (remaning % 3)

    est_longest_small_steps = 0
    est_smallest_small_steps = 0

    est = est_longest_large_steps * 4 + est_longest_small_steps + est_smallest_large_steps * 4 + est_smallest_small_steps

    return est

def heuristic_manhattan(pos, goal):
    return cityblock(pos, goal)

def heuristic_zero(pos, goal):
    return 0

def a_star(start, goal):
    explored = set()
    to_explore = [] # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (heuristic_zero(start, goal), 0, start, EAST, 1))
    heapq.heappush(to_explore, (heuristic_zero(start, goal), 0, start, SOUTH, 1))

    while len(to_explore) > 0:
        estimated_cost, cost_so_far, pos, direction, n_straight = heapq.heappop(to_explore)
        if pos == goal:
            print("FOUND")
            return cost_so_far

        # explored.add((pos, direction, n_straight))

        actions = get_next_actions(pos, direction, n_straight)
        for next_pos, next_direction, next_straight in actions:
            if (next_pos, next_direction, next_straight) in explored: # don't explore again
                continue
            cost = city[next_pos[0], next_pos[1]]
            next_cost_so_far = cost_so_far + cost
            heapq.heappush(to_explore, (heuristic_zero(next_pos, goal) + next_cost_so_far, next_cost_so_far, next_pos, next_direction, next_straight))
            explored.add((next_pos, next_direction, next_straight)) # TODO: this is only possible without heuristc i think
    return "Not found"



start = (0, 0)
goal = (height - 1, width - 1)

start_time = time.time()

print(a_star(start, goal))

print("--- %s seconds ---" % (time.time() - start_time))



# 1256
# 1382