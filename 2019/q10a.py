import math
from itertools import permutations

from matplotlib import pyplot as plt

from tools.advent_tools import *

file1 = open('q10a.txt', 'r')
lines = file1.readlines()

astroids, width, height = read_grid(lines, GRID_SET, f_prepare_line=lambda x: x.rstrip(), value_conversions={"#": 1, ".": None}, int_conversion=False)

astroids = list(astroids)

angles = {}

for i in range(len(astroids)):
    i1, j1 = astroids[i]
    angles[astroids[i]] = set()
    for j in range(len(astroids)):
        if i == j:
            continue # skip self
        i2, j2 = astroids[j]

        angle = math.atan2((i2 - i1), (j2 -j1))
        angles[astroids[i]].add(angle)

sizes = [len(x) for x in angles.values()]


print("Part 1", max(sizes))

index_max = np.argmax(sizes)

station = list(angles.keys())[index_max]

print(station)

i1, j1 = station

# find target angles and distances
targets = {}
for n in range(len(astroids)):
    if astroids[n] == station:
        continue # skip self

    i2, j2 = astroids[n]
    angle = math.atan2((i1 - i2), (j1 -j2)) # swap them to start 0 degrees left
    # if angle < 0:
    #     angle = (2 * math.pi) - angle # make negative angles positive so we get 0-2pi
    distance = math.sqrt((i2 - i1)*(i2 - i1) + (j2 -j1)*(j2 -j1))

    # # TODO: hij begint niet links, maar omhoog
    # angle -= 0.5 * math.pi
    # if angle < 0:
    #     angle = (2 * math.pi) - angle


    if angle in targets:
        targets[angle].append((distance, (i2, j2)))
    else:
        targets[angle] = [(distance, (i2, j2))]

print(targets)

# sort distances (smallest distance gets shot first)
for angle in targets:
    targets[angle].sort()

print(">", targets)

# test atan2

sorted_angles = sorted(list(targets.keys()))

# TODO: change order
zero = sorted_angles.index(0.5 * math.pi)

sorted_angles = sorted_angles[zero:] + sorted_angles[0: zero]



print(sorted_angles)



destroyed = []
while True:
    destroyed_something = False
    for i in range(len(sorted_angles)):
        angle = sorted_angles[i]
        if len(targets[angle]) > 0: # there must be astroids left
            _, astroid = targets[angle].pop(0)
            destroyed.append(astroid)
            print(f"{len(destroyed)}. {astroid[1]}, {astroid[0]}")
            destroyed_something = True
        # else:
        #     print("no astroids at this angle left")
        # if len(destroyed) == 200:
        #     break
    if destroyed_something:
        break

print(destroyed)



x = []
y = []
for i, j in destroyed:
    x.append(j)
    y.append(i)



plt.plot(x, y)
plt.show()

# print(destroyed)

i, j = destroyed[199]
print(f"Part 2 {j, i}", j * 100 + i)