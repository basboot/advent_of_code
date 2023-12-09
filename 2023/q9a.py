# Using readlines()

file1 = open('q9a.txt', 'r')
lines = file1.readlines()

import numpy as np

total = 0
for line in lines:
    y = np.array([int(y) for y in line.rstrip().split(" ")])

    memory = np.zeros((len(y), len(y)))
    memory[0,:] = y

    # repeat subtracting right values from left values
    for i in range(1,len(y)):
        right = memory[i - 1, i:]
        left = memory[i - 1, i - 1:-1]
        memory[i,i:] = right - left

    # we can just sum them all up in the right row, instead of one by one
    new_y = sum(memory[1:, -1]) + memory[0,-1]

    total += new_y

print("Part 1", total)

# Part 2, other side
total = 0
for line in lines:
    y = np.array([int(y) for y in line.rstrip().split(" ")])

    memory = np.zeros((len(y), len(y)))
    memory[0,:] = y

    for i in range(1,len(y)):
        right = memory[i-1, 1:len(y) - i + 1]
        left = memory[i-1,0:-i]
        memory[i,:-i] = right - left

    # because we have to substract pairwise we cannot use the trick from before
    new_y = 0
    for i in range(len(y)):
        new_y = memory[len(y) - 1 - i, 0] - new_y

    total += new_y

print("Part 2", total)