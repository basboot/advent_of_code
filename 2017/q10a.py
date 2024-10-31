from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q10a.txt', 'r')
lengths = [int(x) for x in file1.readlines()[0].rstrip().split(", ")]


print(lengths)

SIZE = 5

PREV, VALUE, NEXT, FORWARD = 0, 1, 2, 3
list = [[(x-1) % SIZE, x, (x+1) % SIZE, x == 0] for x in range(SIZE)]

print(list)

position = 0
skip_size = 0

length = lengths[0]

temp_prev = list[position][PREV]
next_position = position
for i in range(length):
    temp_next = list[next_position][NEXT]
    list[next_position][NEXT] = list[next_position][PREV]
    list[next_position][PREV] = temp_next
    if i < length - 1: # skip last, to have position-next_position as start an finish of reversed part
        next_position = temp_next

print(list)
print(next_position)
print(list[next_position][PREV])

# fix boundary points
list[position][NEXT] = list[next_position][PREV]
list[next_position][PREV] = temp_prev
print(list)

# now fix boundary +- 1
plus_one = list[position][NEXT]
minus_one = list[next_position][PREV]
list[plus_one][PREV] = position
list[minus_one][NEXT] = next_position

# move pointer with length
position = plus_one

# move pointer with skip_size
for i in range(skip_size):
    next_position = list[next_position][NEXT]

# update skip_size
skip_size += 1


print("POS", position)




position = 0
for i in range(len(list)):
    print(list[position][VALUE], end=", ")
    position = list[position][NEXT]

print()


