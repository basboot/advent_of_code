from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q10a.txt', 'r')
lengths = [int(x) for x in file1.readlines()[0].rstrip().split(",")]


print(lengths)

SIZE = 256

list = list(range(SIZE))


position = 0
skip_size = 0

length = lengths[0]

def swap_list(start, length, list):
    for i in range(length // 2):
        temp = list[(start + i) % SIZE]
        list[(start + i) % SIZE] = list[(start + length - i - 1) % SIZE]
        list[(start + length - i - 1) % SIZE] = temp

print(list)

for length in lengths:
    swap_list(position, length, list)
    position = (position + length + skip_size) % SIZE
    print(position)
    print(list)
    skip_size += 1

print("Part 1", list[0] * list[1])

# 63756 too high
# 11413