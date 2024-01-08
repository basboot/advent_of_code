from bitstring import BitArray

file1 = open('q3a.txt', 'r')
lines = file1.readlines()

import numpy as np

result = None


for row in lines:
    np_row = np.array([int(x) for x in row.rstrip()])
    if result is None:
        result = np_row
    else:
        result = result + np_row

gamma = (BitArray(bin="".join([str(int(x)) for x in list(np.round(result / len(lines)))]))).uint
epsilon = (BitArray(bin="".join([str((1 - int(x))) for x in list(np.round(result / len(lines)))]))).uint

print(gamma * epsilon)