import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q15a.txt', 'r')

disks = []
for line in file1.readlines():
    disks.append((int(line.rstrip().split(" ")[3]), int(line.rstrip().replace(".", "").split(" ")[11])))

print(disks)

# Part 2

disks.append((11, 0))


# just trying first
t = 0
while True:
    found = True
    for i in range(len(disks)):
        disk_size, disk_start = disks[i]

        time_at_disk = t + 1 + i
        if (time_at_disk + disk_start) % disk_size != 0:
            found = False
            break

    if found:
        print("Part 1/2", t)
        break
    t += 1


