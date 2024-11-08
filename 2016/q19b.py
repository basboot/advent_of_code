import hashlib
import math
from collections import Counter, deque

import numpy as np

import networkx as nx
from collections import defaultdict



n_elves = 3004953

elves = [True] * n_elves # Zero indexed, so add one at the end!

current_elve = n_elves // 2

for i in range(n_elves - 1): # remove all elves but one
    elves[current_elve] = False
    elves_left = n_elves - i - 1
    steps = 2 if elves_left % 2 == 0 else 1
    while steps > 0:
        current_elve = (current_elve + 1) % n_elves
        if elves[current_elve]:
            steps -= 1


    # print(elves)

print("Part 2", elves.index(True) + 1)



