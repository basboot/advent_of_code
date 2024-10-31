import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q13a.txt', 'r')

firewall = []

for line in file1.readlines():
    scanner_depth, scanner_range = [int(x) for x in line.rstrip().split(": ")]
    firewall.append((scanner_depth, scanner_range))



def severity(delay = 0):
    total = 0
    caught = False
    for scanner_depth, scanner_range in firewall:
        if (scanner_depth + delay) % (2 * (scanner_range - 1)) == 0: # caught
            total += scanner_depth * scanner_range
            caught = True
    return total, caught # needed to add caught, because getting caught add depth zero does not add severity

print("Part 1", severity())

delay = 0
while severity(delay)[1]:
    delay += 1

print("Part 2", delay)

# 47400 too low


