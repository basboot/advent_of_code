import math
from itertools import product

from sympy import Symbol, solve
import numpy as np

file1 = open('q22a.txt', 'r')
file_lines = file1.readlines()

cubes = []
for line in file_lines:
    onoff, values = line.rstrip().split(" ")

    # add 50 to remove negative values, so -50, 50 becomes 0, 100
    ranges = [([int(x) + 50 for x in range.split("..")]) for range in values.replace("x=","").replace("y=","").replace("z=","").split(",")]

    cubes.append((1 if onoff == "on" else 0, ranges))

print(cubes)

cuboid = np.zeros((101, 101, 101))

for cube in cubes:
    onoff, ranges = cube
    x, y, z = ranges

    in_range = True
    for first, last in [x, y, z]:
        if first < 0 or last > 100:
            in_range = False

    if in_range:
        print(f"set {x} {y} {z} to {onoff}")
        cuboid[x[0]:x[1] + 1, y[0]:y[1] + 1, z[0]:z[1] + 1] = onoff

print(np.sum(cuboid))

# 590784 too high