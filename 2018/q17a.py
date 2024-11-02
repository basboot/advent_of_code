import sys

sys.setrecursionlimit(20000)

import math
from collections import Counter
import numpy as np

file1 = open('q17a.txt', 'r')
lines = file1.readlines()

clay = set()
water = set()
flowing_water = set()

max_y = math.inf
min_y = -math.inf

WALL, SOURCE = 0, 1

def probe_down(pos):
    x, y = pos
    while y <= max_y:
        if (x, y) in flowing_water:
            break # do not explore again
        flowing_water.add((x, y))
        if (x, y + 1) in clay or (x, y + 1) in water:
            return x, y
        y += 1

    return None

def probe_horizontal(pos, direction):
    x, y = pos
    while True:
        if (x, y + 1) not in clay and (x, y + 1) not in water:
            return (x, y), SOURCE
        if (x + direction, y) in clay:
            return (x + direction, y), WALL # position of wall
        x += direction

def probe_left_right(pos):
    return (probe_horizontal(pos, -1), probe_horizontal(pos, 1))

def start_source(pos):
    pos = probe_down(pos)
    if pos is None:
        return
    fill_water(pos)

def fill_water(pos):
    (pos_left, type_left), (pos_right, type_right) = probe_left_right(pos)
    for xw in range(pos_left[0] + 1, pos_right[0]):
        if type_left == WALL and type_right == WALL:
            water.add((xw, pos[1]))
        else:
            flowing_water.add((xw, pos[1]))

    if type_left == WALL and type_right == WALL:
        if pos[1] - 1 > min_y:
            fill_water((pos[0], pos[1] - 1))
    if type_left == SOURCE:
        start_source(pos_left)
    if type_right == SOURCE:
        start_source(pos_right)



# x=495, y=2..7
for line in lines:
    left, right = line.rstrip().split(", ")
    direction, coordinate_string = left.split("=")
    coordinate = int(coordinate_string)
    start_range, end_range = [int(x) for x in right.split("=")[1].split("..")]
    coordinate_range = range(start_range, end_range + 1) # +1 because inclusive

    # print(direction, coordinate, coordinate_range)

    for i in coordinate_range:
        clay.add((coordinate, i) if direction == "x" else (i, coordinate))

# print(clay)

# reduce max depth
max_y = min(max_y, max([y for x, y in clay]))
min_y = max(min_y, min([y for x, y in clay]))

start_source((500, 0))

# print(flowing_water)

print(len(water))
print(len([pos for pos in water.union(flowing_water) if min_y <= pos[1] <= max_y])) # - 1 for source







# for y in range(-10, int(max_y) + 10):
#     for x in range(420, 580):
#         if (x, y) in clay:
#             print("#", end="")
#         else:
#             if (x, y) in water:
#                 print("~", end="")
#             else:
#                 if (x, y) in flowing_water:
#                     print("|", end="")
#                 else:
#                     print(".", end="")
#     print()




# 369 too low
# 31790 too high => error, all above min_y must be removed