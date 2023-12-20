# Using readlines()
import math
import sys
import numpy as np

from scipy.spatial.distance import cityblock

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

map, width, height = read_grid(lines, GRID_DICT, lambda a: a.strip())


WIND_CONVERSION = {
    ">": EAST,
    "<": WEST,
    "^": NORTH,
    "v": SOUTH
}
winds = []
# on update create occupied set
valley = set()

def update_winds(winds):
    occupied = set()
    next_winds = []
    for w in range(len(winds)):
        # get wind props
        i, j, di, dj = winds[w]
        # update position
        ni, nj = i + di, j + dj
        # move to other side when it has reached te end
        if ni == 0:
            ni = height - 2
        if nj == 0:
            nj = width - 2
        if ni == height - 1:
            ni = 1
        if nj == width - 1:
            nj = 1

        # update wind
        next_winds.append((ni, nj, di, dj))
        occupied.add((ni, nj))

    return next_winds, occupied


# create winds array and
for key, value in map.items():
    print(key, "->", value)
    if value == ".":
        continue
    if value == "#":
        valley.add(key)
        continue

    direction = DIRECTIONS[WIND_CONVERSION[value]]
    winds.append((key[0], key[1], direction[0], direction[1]))

print(valley)
print(winds)
winds_repeat_pattern = np.lcm.reduce([height - 2, width - 2])

def draw_valley(pos):
    for i in range(height):
        for j in range(width):
            if pos is not None and pos == (i, j):
                print("E", end="")
                continue
            if (i, j) in valley:
                print("#", end="")
            else:
                wind_shown = False
                for iw, jw, diw, djw in winds:
                    if (i, j) == (iw, jw):
                        print("*", end="")
                        wind_shown = True
                        break
                if not wind_shown:
                    print(" ", end="")
        print()

# close the valley, so we don't have to check the boundaries
valley.add((-1, 1))

start = (0,1)
goal = (height - 1, width - 2)

shortest_length = math.inf

lookup_table = {

}

# no visited possible i think, but try anyway
def dfs(current_pos, winds, visited, length, route, wind_pattern):
    global shortest_length
    if current_pos == goal:
        print("FOUND", current_pos, len(route), route)
        shortest_length = min(length, shortest_length)
        return length, route  #TODO: denk na

    # we cannot use visited because you need to avoid blizards, this we force not wandering forever
    if length + cityblock(current_pos, goal) > shortest_length:
        return math.inf, []

    # visited.add(current_pos)

    i, j = current_pos

    # update winds
    next_winds, winds_occupied = update_winds(winds)

    # find next positions
    next_positions = []
    for direction in DIRECTIONS:
        di, dj = DIRECTIONS[direction]
        ni, nj = i + di, j + dj
        next_pos = (ni, nj)

        if next_pos not in valley and next_pos not in winds_occupied and next_pos not in visited:
            next_positions.append((cityblock(next_pos, goal), next_pos))

    # we can also wait if there is no wind
    if current_pos not in winds_occupied:
        next_positions.append((cityblock(current_pos, goal), current_pos))

    # try to help by prioritizing actions towards the goal
    next_positions.sort()


    min_steps = math.inf
    min_route = []
    for distance_and_next_position in next_positions:
        dist, next_position = distance_and_next_position
        i, j = next_position

        next_wind_pattern = (wind_pattern + 1) % winds_repeat_pattern # avoid walking in circles

        if (i, j, wind_pattern) in visited:
            continue

        new_route = route.copy()
        new_route.append(next_position)
        new_visited = visited.copy()
        new_visited.add((i, j, wind_pattern))
        steps, other_route = dfs(next_position, next_winds, new_visited, length + 1, new_route, next_wind_pattern)

        if steps < min_steps:
            min_steps = steps
            min_route = other_route

    return min_steps, min_route



steps, route = dfs(start, winds, set(), 0, [start], 0)

print(steps, route)

# i = 0
#
# for pos in route:
#     print(i, pos, "--------")
#     draw_valley(pos)
#     winds, _ = update_winds(winds)
#     i += 1