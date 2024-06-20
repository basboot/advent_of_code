import math
from functools import cache
from itertools import permutations

import numpy as np

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

signal = np.array(([int(x) for x in list(lines[0].rstrip())] * 10000))

offset = int("".join(list(lines[0].rstrip())[0:7])) # is index of the first digit needed
print(offset)
print(len(signal))
print(len(signal) - offset)

# only the part and below are usefull for us (others are multiplied by the leading zeros in the pattern)
reduced_signal = signal[offset:]
print(reduced_signal)

# last row in pattern is 0's and 1, next is zeros and 2x1, etc, so we can do a cum sum instead of multiplication
# on the reverse
reversed_reduced_signal = np.flip(reduced_signal)

# do 100x + abs mod 10
for _ in range(100):
    reversed_reduced_signal = np.mod(np.abs(np.cumsum(reversed_reduced_signal)), 10)

# flip result back
result_signal = np.flip(reversed_reduced_signal)

print("".join([str(x) for x in list(result_signal[0:8])]))