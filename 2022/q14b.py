import math
from ast import literal_eval

import numpy

# Using readlines()
file1 = open('q14a.txt', 'r')
lines = file1.readlines()

cave = {}

ROCK = 1
SAND = 2

def add_rocks(from_p, to_p):
    assert  from_p[0] == to_p[0] or from_p[1] == to_p[1], "only straight lines allowed"

    current_p = list(from_p)

    while tuple(current_p) != to_p:
        cave[tuple(current_p)] = ROCK
        current_p[0] += numpy.sign(to_p[0] - current_p[0])
        current_p[1] += numpy.sign(to_p[1] - current_p[1])

    # add last
    cave[tuple(current_p)] = ROCK

MAX_DROP = 1000

def drop_sand(p):
    current_p = list(p)
    count = 0
    while count < MAX_DROP:
        count += 1
        if (current_p[0], current_p[1] + 1) not in cave:
            # drop down is possible
            current_p[1] += 1
        else:
            if (current_p[0] - 1, current_p[1] + 1) not in cave:
                # drop down left
                current_p[0] -= 1
                current_p[1] += 1
            else:
                if (current_p[0] + 1, current_p[1] + 1) not in cave:
                    # drop down right
                    current_p[0] += 1
                    current_p[1] += 1
                else:
                    # no drop possible
                    break
    if count < MAX_DROP:
        # add sand
        cave[tuple(current_p)] = SAND
        if tuple(current_p) == (500, 0):
            return False
        else:
            return True
    else:
        assert True, "Sand keeps falling, floor is not sealed"





highest_y = -math.inf
for line in lines:
    row = line.rstrip()
    # print("input: ", row)
    # print(row.split(" -> "))

    prev_p = None
    for point in row.split(" -> "):
        p = literal_eval(f"({point})")
        highest_y = max(highest_y, p[1])
        if prev_p is not None:
            # print(f"rocks from {prev_p} to {p}")
            add_rocks(prev_p, p)

        prev_p = p

# print(highest_y)
# You don't have time to scan the floor, so assume the floor is an infinite horizontal line with
# a y coordinate equal to two plus the highest y coordinate of any point in your scan.
# (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.)

add_rocks((-1000, highest_y + 2), (1000, highest_y + 2))


i = 0
while drop_sand((500, 0)):
    i += 1

print("Part 2", i + 1)






