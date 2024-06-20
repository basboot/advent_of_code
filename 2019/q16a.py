import math
from functools import cache
from itertools import permutations

import numpy as np

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

signal = np.array([int(x) for x in list(lines[0].rstrip())])


@cache
def create_pattern_matrix(length):
    pattern_matrix = []
    for element in range(1, length + 1):
        pattern = []
        while len(pattern) < (length + 1): # +1, because we need to skip the first
            for digit in [0, 1, 0, -1]:
                for i in range(element):
                    pattern += [digit]

        # skip first, and cut at length
        pattern = pattern[1: 1 + length]
        pattern_matrix.append(pattern)

    return np.array(pattern_matrix)

# print(signal)

pattern = create_pattern_matrix(len(signal))

for i in range(100):
    signal = np.mod(np.abs(np.dot(pattern, np.transpose(signal))), 10)

print(signal)

print("Part 1", "".join([str(x) for x in signal[0:8]]))



# TODO: dit ziet eruit als een matrix vermenigvuldiging!
# TODO: dus pattern kan meteen voor hele dom gemaakt worden!
# Daarna abs + mod