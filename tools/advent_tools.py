import math

import numpy as np

GRID_LIST, GRID_NUMPY, GRID_DICT = 0, 1, 2

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

DIRECTIONS = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}


# return (next_pos), move_possible
def next_pos(current_pos, direction, width, height):
    i, j = current_pos
    di, dj = DIRECTIONS[direction]
    next_i, next_j = i + di, j + dj

    if 0 <= next_i < height and 0 <= next_j < width:
        return (next_i, next_j), True
    else:
        return (i, j), False

def read_grid(input, grid_type, f_prepare_line=None, value_conversions=None, data_conversions=None):

    if grid_type == GRID_DICT:
        grid = {}
    else:
        assert True, "Not implemented"

    width = -math.inf
    height = -math.inf

    for i in range(len(input)):
        line = input[i]
        row = f_prepare_line(line) if f_prepare_line is not None else line

        height = max(height, i)

        for j in range(len(row)):

            width = max(width, j)

            if grid_type == GRID_DICT:
                grid[(i, j)] = row[j]
            else:
                assert True, "Not implemented"

    return grid, width + 1, height + 1