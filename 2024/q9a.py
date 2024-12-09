import numpy as np

file1 = open('q9a.txt', 'r')
line = file1.readlines()[0].rstrip() + "0" # add zero for missing empty spot at end

disk = []

for i, files_free in enumerate(zip(line[0::2], line[1::2])):
    disk += [i] * int(files_free[0]) + [-1] * int(files_free[1])

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

for i, value in enumerate(disk):
    if value == -1:
        break
    else:
        total += value * i

print(f"Part 1, {total}")

# 6259530434615 too low