# Using readlines()
from scipy.spatial.distance import cityblock

file1 = open('q11a.txt', 'r')
lines = file1.readlines()

import itertools

observations = set()

# keep track of used rows/cols to easily find unused ones
used_rows = set()
used_cols = set()

# row/col before expansion => after expansion
row_conversions = {}
col_conversions = {}


width = 0 # with of the observations

height = len(lines) # height of the observations
for i in range(len(lines)):
    row = list(lines[i].rstrip())
    # print(row)
    width = len(row)
    for j in range(len(row)):
        if row[j] == "#": # add galaxy and update row/col usage
            observations.add((i, j))
            used_rows.add(i)
            used_cols.add(j)


# times larger - 1 (real row/col)
# EXPANSION = 2 - 1 # part 1
EXPANSION = 1000000 - 1 # part 2

# create conversion
i_offset = 0
for i in range(height):
    j_offset = 0
    if i not in used_rows:
        i_offset += EXPANSION
    for j in range(width):
        if j not in used_cols:
            j_offset += EXPANSION

        row_conversions[i] = i + i_offset
        col_conversions[j] = j + j_offset


# count distances after exapansion between all combinations of galaxies
total = 0
for combination in itertools.combinations(observations, 2):
    # print(combination)
    ((i1, j1), (i2, j2)) = combination

    distance = cityblock((row_conversions[i1], col_conversions[j1]), (row_conversions[i2], col_conversions[j2]))

    total += distance

print(total)