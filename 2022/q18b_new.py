# Using readlines()
import sys

sys.setrecursionlimit(100000)

file1 = open('q18a.txt', 'r')
lines = file1.readlines()

# naive approach but maybe it works

cubes = {}

directions = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]

def calculate_postion(pos, dir, reverse=False):
    return (
        pos[0] + (dir[0] if not reverse else -dir[0]),
        pos[1] + (dir[1] if not reverse else -dir[1]),
        pos[2] + (dir[2] if not reverse else -dir[2]),
    )

def invert_direction(dir):
    return (-dir[0], -dir[1], -dir[2])

MIN = -2
MAX = 22

def legal_position(position):
    x, y, z = position
    return MIN < x < MAX and MIN < y < MAX and MIN < z < MAX


def expand_water(position):
    if position in cubes:
        assert True, "I don't think this can happen"
        return

    # create water
    cubes[position] = {}
    cubes[position]["lava"]=  False

    for direction in directions:
        new_position = calculate_postion(position, direction)

        # skip illegal positions
        if not legal_position(position):
            continue

        # only explore empty spaces
        if new_position not in cubes:
            expand_water(new_position)
        else:
            # only update lava, water can be ignored
            if cubes[new_position]["lava"]:
                cubes[new_position][invert_direction(direction)] = True # water reaches lava from other side


for line in lines:
    x, y, z = [int(p) for p in line.rstrip().split(",")]

    assert (x, y, z) not in cubes, "Same cube seen twice"

    # create cube
    cubes[(x, y, z)] = {}

    for direction in range(len(directions)):
        cubes[(x, y, z)][directions[direction]] = False # True is reachable
        cubes[(x, y, z)]["lava"] = True # True is lava, False is water


# droplet within 0-20,0-20,0-20 for main assignment

expand_water((-1, -1, -1))


total = 0
for position in cubes:
    # only count lava
    if not cubes[position]["lava"]:
        continue

    for direction in directions:
        if cubes[position][direction]:
            total += 1

print("Part 2", total)