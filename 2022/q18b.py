# Using readlines()
import math

from collections import deque

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

for line in lines:
    x, y, z = [int(p) for p in line.rstrip().split(",")]

    # # ignore cubes already seen
    # if (x, y, z) in cubes:
    #     continue

    assert (x, y, z) not in cubes, "Same cube seen twice"

    # create cube
    cubes[(x, y, z)] = {}

    for i in range(len(directions)):
        direction = directions[i] # TODO: needs to be converted to position!!!
        position = calculate_postion((x, y, z), directions[i])
        if position not in cubes:
            cubes[(x, y, z)][direction] = True # True is visible
        else:
            cubes[(x, y, z)][direction] = False
            assert cubes[position][invert_direction(directions[i])], f"Side already connected"
            cubes[position][invert_direction(directions[i])] = False



total = 0
for position in cubes:
    for direction in cubes[position]:
        if cubes[position][direction]:
            total += 1
            # reset cubes
            cubes[position][direction] = False

print("Part 1", total)


print(cubes)

# find min and max values
min_x = min_y = min_z = math.inf
max_x = max_y = max_z = -math.inf

for position in cubes:
    x, y, z = position
    min_x = min(x, min_x)
    min_y = min(y, min_y)
    min_z = min(z, min_z)

    max_x = max(x, max_x)
    max_y = max(y, max_y)
    max_z = max(z, max_z)

MIN = min([min_x, min_y, min_z])
MAX = max([max_x, max_y, max_z])

print(MIN, MAX)





for dir in range(6):
    # create water plane
    water = {}
    for i in range(MIN, MAX + 1):
        for j in range(MIN, MAX + 1):
            water[(i, j)] = True

    direction = directions[dir] # x, -x, y, -y, z, -z

    pos_range = range(MIN, MAX + 1) if dir % 2 == 0 else range(MAX, MIN - 1, -1)

    for pos in pos_range:
        for i in range(MIN, MAX + 1):
            for j in range(MIN, MAX + 1):
                pos_d = deque([pos, i, j]) # put pos in dequeue
                pos_d.rotate(dir // 2) # rotate 0, 1, 2 for x, y, z
                pos_water = tuple(pos_d)
                # print(pos_water)
                if pos_water in cubes and water[(i, j)]:
                    # print("cool")
                    water[(i, j)] = False # only cool 1
                    cubes[pos_water][invert_direction(direction)] = True # cool side

print(cubes)


total = 0
for position in cubes:
    for direction in cubes[position]:
        if cubes[position][direction]:
            total += 1
            # reset cubes
            cubes[position][direction] = False

print("Part 2", total)

# Not correct, apparently steam can do corners TODO: other approach




