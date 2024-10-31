from collections import defaultdict

import numpy as np
from numpy.core.defchararray import isnumeric

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

t = 2503

results = []

for line in lines:
    name, _, _, speed, _, _, duration, _, _, _, _, _, _, rest, _ = line.rstrip().split(" ")

    print(name, speed, duration, rest)

    flight_time = (t // (int(duration) + int(rest))) * int(duration) + min((t % (int(duration) + int(rest))), int(duration))
    print(flight_time * int(speed))

    results.append((flight_time * int(speed), name))

results.sort(reverse=True)

print(f"Part 1: {results[0][1]} wins with distance {results[0][0]}")