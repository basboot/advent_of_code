# Using readlines()
from numpy.polynomial import Polynomial

file1 = open('q9a.txt', 'r')
lines = file1.readlines()

import numpy as np
from scipy.interpolate import lagrange

total = 0
for line in lines:
    y = np.array([int(y) for y in line.rstrip().split(" ")])
    x = range(len(y))
    # print(y)
    poly = lagrange(x, y)
    # print("------")
    new_y = Polynomial(poly.coef[::-1])(len(y))
    # print(round(new_y))

    total += new_y

print("Part 1", total)

# Lagrange niet nauwkeurig genoeg :-(
# 1877791528 too low
# 1877791534 too low
# 1877791533.9415786

# 1877825184