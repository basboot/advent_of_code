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

    if is_valid_pos((next_i, next_j), width, height):
        return (next_i, next_j), True
    else:
        return (i, j), False

def is_valid_pos(pos, width, height):
    i, j = pos
    return 0 <= i < height and 0 <= j < width

def read_grid(input, grid_type, f_prepare_line=None, value_conversions=None, int_conversion=True):

    if grid_type == GRID_DICT:
        grid = {}
    else:
        if grid_type == GRID_NUMPY or grid_type == GRID_LIST:
            grid = []
        else:
            assert True, "Not implemented"

    width = -math.inf
    height = -math.inf

    for i in range(len(input)):
        line = input[i]
        row = f_prepare_line(line) if f_prepare_line is not None else line

        height = max(height, i)

        if grid_type == GRID_NUMPY or grid_type == GRID_LIST:
            grid_row = []

        for j in range(len(row)):

            width = max(width, j)

            value = row[j]

            if value_conversions is not None:
                assert value in value_conversions, f"Value missing in conversion {value}"
                value = value_conversions[value]

            if int_conversion:
                value = int(value)

            if grid_type == GRID_DICT:
                grid[(i, j)] = value
            else:
                if grid_type == GRID_NUMPY or grid_type == GRID_LIST:
                    grid_row.append(value)
                else:
                    assert True, "Not implemented"

        if grid_type == GRID_NUMPY or grid_type == GRID_LIST:
            grid.append(grid_row)

    if grid_type == GRID_NUMPY:
        grid = np.array(grid)

    if grid_type == GRID_LIST:
        if len(grid) == 1:
            grid = grid[0]

    return grid, width + 1, height + 1