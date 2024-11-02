from collections import Counter
import numpy as np

file1 = open('q2a.txt', 'r')
lines = file1.readlines()

two = 0
three = 0

for line in lines:
    counts = set(Counter(line.rstrip()).values())
    if 2 in counts:
        two += 1
    if 3 in counts:
        three += 1

print("Part 1", two * three)


ids = []
for line in lines:
    id = line.rstrip()
    id_nums = [ord(x) for x in id]
    ids.append(np.array(id_nums))

for i in range(len(ids)):
    for j in range(len(ids)):
        if i == j:
            continue # do not compare same ids
        comparison = ids[i] - ids[j]
        if np.sum(comparison != 0) == 1: # look for 1 difference
            print(lines[i], lines[j])


# rtehotyxzbodglnpkudawhijsc
# rtefotyxzbodglnpkudawhijsc

# rteotyxzbodglnpkudawhijsc




