import math

import numpy as np

GRID_LIST, GRID_NUMPY, GRID_DICT, GRID_SET = 0, 1, 2, 3

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

DIRECTIONS = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}


# return (next_pos), move_possible
def next_pos(current_pos, direction, width=None, height=None):
    i, j = current_pos
    di, dj = DIRECTIONS[direction]
    next_i, next_j = i + di, j + dj

    if width is None or is_valid_pos((next_i, next_j), width, height):
        return (next_i, next_j), True
    else:
        return (i, j), False

def is_valid_pos(pos, width, height):
    i, j = pos
    return 0 <= i < height and 0 <= j < width

def read_grid(input, grid_type, f_prepare_line=None, value_conversions=None, int_conversion=False):

    if grid_type == GRID_DICT or grid_type == GRID_SET:
        if grid_type == GRID_DICT:
            grid = {}
        else:
            grid = set()
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
                if value is None: # skip None values (only makes sense dict)
                    continue

            if int_conversion:
                value = int(value)

            if grid_type == GRID_DICT or grid_type == GRID_SET:
                if grid_type == GRID_DICT:
                    grid[(i, j)] = value
                else:
                    grid.add((i, j))
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

# section = (x_start, x_end)
def find_overlap(section1, section2):
    if section1[0] < section2[0]:
        start_section = section1
        end_section = section2
    else:
        start_section = section2
        end_section = section1

    if start_section[0] < end_section[0]:
        part1 = [start_section[0], min(start_section[1], end_section[0])]
    else:
        part1 = None

    if start_section[0] < end_section[1] and start_section[1] > end_section[0]:
        part2 = [max(start_section[0], end_section[0]), min(start_section[1], end_section[1])]
    else:
        part2 = None

    if start_section[1] != end_section[1]:
        if part2 is None: # no overlap, just return
            part3 = [end_section[0], end_section[1]]
        else:
            part3 = [min(start_section[1], end_section[1]), max(start_section[1], end_section[1])]
    else:
        part3 = None

    return part1, part2, part3


if __name__ == '__main__':
    print(find_overlap([1, 4], [2, 5]))
    print(find_overlap([4, 5], [1, 10]))
    print(find_overlap([1, 2], [10, 11]))
    print(find_overlap([5, 10], [2, 7]))
    print(find_overlap([3, 5], [1, 12]))
    print(find_overlap([4, 8], [4, 8]))
    print(find_overlap([1, 8], [4, 8]))
    print(find_overlap([4, 8], [4, 12]))

