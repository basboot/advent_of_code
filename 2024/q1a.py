import numpy as np

file1 = open('q1a.txt', 'r')
lines = file1.readlines()

lists = [[], []]

for line in lines:
    for i, n in enumerate([int(x) for x in line.rstrip().split("   ")]):
        lists[i].append(n)

# align listst and make np arrays for calculation
np_lists = [np.array(sorted(l)) for l in lists]

# sum up distances between numbers in lists
total = np.sum(np.abs(np_lists[0] - np_lists[1]))

print(f"Part 1, sum of distances = {total}")
