from tools.advent_tools import *

file1 = open('q3a.txt', 'r')
lines = file1.readlines()

forrest, width, height = read_grid(lines, GRID_SET, f_prepare_line=lambda x: x.rstrip(),
                                   value_conversions={"#": True, ".": False}, int_conversion=False)


print(width, height)
print(forrest)



trees_prod = 1
for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
    pos = (0, 0)
    n_trees = 0
    while pos[0] < height:
        if pos in forrest:
            n_trees += 1
        pos = pos[0] + slope[0], (pos[1] + slope[1]) % width

    print("Part 1", slope, n_trees)
    trees_prod *= n_trees

print("Part 2", trees_prod)

# 97050312 too low