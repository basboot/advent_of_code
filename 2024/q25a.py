from itertools import product

import numpy as np

file1 = open('q25a.txt', 'r')
lines = file1.read()

lines = [list(map(int, list(x))) for x in lines.replace("#", "1").replace(".", "0").split("\n")]

keys = []
locks = []

for i in range(0, len(lines), 8):
    row = np.array(lines[i: i + 7])

    if np.sum(row, 1)[0] == 5:
        locks.append(np.sum(row, 0) - 1)
    else:
        keys.append(np.sum(row, 0) - 1)

total = 0

for lock, key in product(locks, keys):
    if np.sum(lock + key > 5) == 0:
        total += 1


print(f"Part 1, {total}")
