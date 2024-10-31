import math
from collections import Counter
from functools import reduce

import numpy as np

import networkx as nx
from collections import defaultdict

a = 65
b = 8921

# Generator A starts with 679
# Generator B starts with 771

a = 679
b = 771

fa = 16807
fb = 48271

modulus = 2147483647

def gen_next(n, factor):
    return (n * factor) % modulus

total = 0

for i in range(40000000):
    a = gen_next(a, fa)
    b = gen_next(b, fb)

    if a & 0b1111111111111111 == b & 0b1111111111111111:
        total += 1

print("Part 1", total)




