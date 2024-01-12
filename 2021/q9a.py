from tools.advent_tools import *

file1 = open('q9a.txt', 'r')
lines = file1.readlines()

heightmap, width, height = read_grid(lines, GRID_NUMPY, lambda a: a.strip(), value_conversions=None, int_conversion=True)

print(heightmap)

risk_levels = 0
basins = []

def find_basin(point, visited):
    visited.add(point)
    i, j = point
    for direction in DIRECTIONS:
        (n_i, n_j), valid = next_pos((i, j), direction, width, height)
        if (n_i, n_j) in visited:
            continue
        if not valid:
            continue
        if heightmap[n_i, n_j] == 9:
            continue
        find_basin((n_i, n_j), visited)
    return visited


for i in range(height):
    for j in range(width):
        low_point = True
        value = heightmap[i, j]
        for direction in DIRECTIONS:
            (n_i, n_j), valid = next_pos((i, j), direction, width, height)
            if not valid:
                continue
            if heightmap[n_i, n_j] <= value:
                low_point = False
                break
        if low_point:
            risk_levels += value + 1
            basin = find_basin((i, j), set())
            # print(basin)
            basins.append(len(basin))

print("Part 1", risk_levels)
basins.sort(reverse=True)
print("Part 2", basins[0] * basins[1] * basins[2])
