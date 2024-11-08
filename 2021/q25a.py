import math

import numpy as np

file1 = open('q25a.txt', 'r')
file_lines = file1.readlines()

width = -math.inf
height = -math.inf

for i in range(len(file_lines)):
    height = max(i + 1, height)
    line = file_lines[i].rstrip()
    for j in range(len(line)):
        width = max(width, j + 1)

east = np.zeros((height, width), dtype=int)
south = np.zeros((height, width), dtype=int)


for i in range(len(file_lines)):
    height = max(i, height)
    line = file_lines[i].rstrip()
    for j in range(len(line)):
        if line[j] == ">":
            east[i, j] = 1
        if line[j] == "v":
            south[i, j] = 1

i = 0
while True:
    i += 1
    # east first
    next_east = np.roll(east, 1, axis=1) # roll east
    wrong = np.bitwise_and(next_east, np.bitwise_or(east, south)) # find overlap with previous all
    next_east = next_east - wrong # remove overlap
    corrected = np.roll(wrong, -1, axis=1) # correct overlap
    next_east = next_east + corrected # restore corrected

    # south after
    next_south = np.roll(south, 1, axis=0) # roll south
    wrong = np.bitwise_and(next_south, np.bitwise_or(next_east, south)) # find overlap with previous all
    next_south = next_south - wrong # remove overlap
    corrected = np.roll(wrong, -1, axis=0) # correct overlap
    next_south = next_south + corrected # restore corrected

    if np.array_equal(np.bitwise_or(east, south), np.bitwise_or(next_east, next_south)):
        print(i)
        break

    east = next_east
    south = next_south
