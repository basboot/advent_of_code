from itertools import chain

import numpy as np

file1 = open('q9a.txt', 'r')
line = file1.readlines()[0].rstrip() + "0" # add zero for missing empty spot at end

disk = list(chain(*[[i] * int(files_free[0]) + [-1] * int(files_free[1]) for i, files_free in enumerate(zip(line[0::2], line[1::2]))]))

last = len(disk) - 1
first = 0

while True:
    # find empty spot
    while disk[first] != -1:
        first += 1
    # ready?
    if first >= last:
        break
    # find non-empty spot
    while disk[last] == -1:
        last -= 1
        # ready?
    if first >= last:
        break
    # swap
    disk[first], disk[last] = disk[last], disk[first]

total = 0


print(f"Part 1, {np.sum((np.array(disk) * np.array(range(len(disk))))[np.array(disk) > 0])}")

# 6259530434615 too low