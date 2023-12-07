# Using readlines()
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

# print(cubes)

total = 0
for position in cubes:
    for direction in cubes[position]:
        if cubes[position][direction]:
            total += 1

print(total)

# 5183 too high



# TODO: count number of exposed cube-surfaces (efficiently!!!)

