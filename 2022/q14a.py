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
        return True
    else:
        return False





for line in lines:
    row = line.rstrip()
    # print("input: ", row)
    # print(row.split(" -> "))

    prev_p = None
    for point in row.split(" -> "):
        p = literal_eval(f"({point})")
        if prev_p is not None:
            # print(f"rocks from {prev_p} to {p}")
            add_rocks(prev_p, p)

        prev_p = p

i = 0
while drop_sand((500, 0)):
    i += 1

print("Part 1", i)



