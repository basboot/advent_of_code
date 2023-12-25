# Using readlines()
import math

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

import re
import numpy as np

REAL = False

VOID, OPEN, WALL = 0, 1, 2
TILES = {" ": VOID, ".": OPEN, "#": WALL }
DIRECTIONS = [NORTH, EAST, SOUTH, WEST] = [3, 0, 1, 2]
deltas = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}

height = 0
width = 0
for i in range(len(lines) - 2):
    height = max(height, i + 1)
    row = list(lines[i].rstrip())
    for j in range(len(row)):
        width = max(width, j + 1)

map = np.zeros((height, width), dtype=object)

cube_size = math.gcd(width, height)


start = (1, 1) # TODO: this could be a wall (although it isn't in the goven problem)
start_rot = None

for i in range(len(lines) - 2):
    row = list(lines[i].rstrip())
    for j in range(len(row)):
        if start is None and TILES[row[j]] == OPEN:
            start = (i, j)
        # encode map coordinates in tile, so we can reconstruct the original position in the cube
        map[i, j] = TILES[row[j]] | (i << 16) | (j << 8)

assert width < 2 ** 8, "Map too large, encoding failed"
assert height < 2 ** 8, "Map too large, encoding failed"

path = re.split('(\d+)', lines[len(lines) - 1].strip())
path.remove("") # remove empty strings at front...
path.remove("") # ...and end

# create cube
# need extra rows, because in a matrix we cannot put different values on the same position
cube = np.zeros((cube_size + 2, cube_size + 2, cube_size + 2), dtype=object) # could be replaced by sparse


def stamp_side(pos, cube, rot_x, rot_y, stamped):
    i, j = pos
    # get side to stamp
    side = map[i: i + cube_size, j: j + cube_size]
    assert side[0, 0] > VOID, "Something went wrong"

    # roll to correct position
    cube = np.rot90(cube, rot_x, (0, 2))
    cube = np.rot90(cube, rot_y, (0, 1))

    # stamp
    cube[0, 1:cube_size + 1, 1:cube_size + 1] = side

    # stamp surrounding map parts by rolling under them
    for di, dj, rx, ry in [(-cube_size, 0, 0, -1), (+cube_size, 0, 0, 1), (0, -cube_size, -1, 0), (0, +cube_size, 1, 0)]:
        next_i, next_j = i + di, j + dj
        if 0 <= next_i < height and 0 <= next_j < width and map[next_i, next_j] & 255 > VOID:
            # print(stamped)
            if ((next_i, next_j)) not in stamped:
                stamped.add((next_i, next_j))
                cube = stamp_side((next_i, next_j), cube, rx, ry, stamped)

    # restore rotation
    cube = np.rot90(cube, -rot_y, (0, 1))
    cube = np.rot90(cube, -rot_x, (0, 2))

    return cube

# find start of map (= first non VOID tile)
map_start = None
for j in range(0, width, cube_size):
    if map[0, j] > VOID:
        map_start = (0, j)
        break
cube = stamp_side(map_start, cube, 0, 0, set(map_start))


def get_new_position(pos, orientation, cube):

    cube_backup = cube.copy() # create backup for easy revert
    direction = deltas[orientation]

    next_i, next_j = pos
    next_orientation = orientation

    next_i, next_j = next_i + direction[0], next_j + direction[1]

    # wrap around the cube, mind the margins
    if next_i < 1:
        next_i = cube_size
        cube = np.rot90(cube, -1, (0, 1))
    if next_j < 1:
        next_j = cube_size
        cube = np.rot90(cube, -1, (0, 2))
    if next_i > cube_size:
        next_i = 1
        cube = np.rot90(cube, 1, (0, 1))
    if next_j > cube_size:
        next_j = 1
        cube = np.rot90(cube, 1, (0, 2))

    if int(cube[0, next_i, next_j]) & 255 == OPEN:
        return (next_i, next_j), next_orientation, cube
    if int(cube[0, next_i, next_j]) & 255 == WALL:
        return pos, orientation, cube_backup

    assert False, "Something went wrong"


# start pos and orientation
pos = start
orientation = EAST


def reconstruct_position(cube, pos, orientation):
    i, j = pos
    # first get the map coorddinates from the higher bytes of the tile
    map_i = (cube[0, i, j] >> 16) & 255
    map_j = (cube[0, i, j] >> 8) & 255


    # then deduct orientation from surroundings
    orientation_offset = 0
    for dir in DIRECTIONS:
        di, dj = deltas[dir]
        prev_i = (cube[0, i + di, j + dj] >> 16) & 255
        prev_j = (cube[0, i + di, j + dj] >> 8) & 255

        # try to reconstruct orientation by looking around. if we are at the border directions can be missing
        # so look for two in opposite directions (east and west)
        if prev_i == map_i and prev_j == map_j + 1:
            # found east
            orientation_offset = dir + EAST

        if prev_i == map_i and prev_j == map_j - 1:
            # found west
            orientation_offset = dir + WEST

    return (map_i, map_j), (orientation - orientation_offset) % 4


for instruction in path:
    if instruction.isnumeric():
        for i in range(int(instruction)):
            new_pos = get_new_position(pos, orientation, cube)
            pos, orientation, cube= new_pos
            show_cube = cube[0, :, :].copy()
            show_cube[pos[0], pos[1]] = 3

    else:
        if instruction == "R":
            orientation = (orientation + 1) % len(DIRECTIONS)
        if instruction == "L":
            orientation = (orientation - 1) % len(DIRECTIONS)

pos, orientation = reconstruct_position(cube, pos, orientation)

print(pos, orientation)

# 1000 times the row, 4 times the column, and the facing.
password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + orientation

print("Part 2", password)
