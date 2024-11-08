from mip import *

from sympy import divisors


def n_presents(n):
    presents = np.array(divisors(n))

    # Part 2
    presents[n / presents > 50] = 0

    return np.sum(presents * 11)

min_presents = 29000000

n = 1

while n_presents(n) < min_presents:
    n += 1

print("Part 1/2", n)