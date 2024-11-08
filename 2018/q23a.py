import math

import numpy as np
from scipy.spatial.distance import cityblock

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

nanobots = []
min_x = min_y = min_z = math.inf
max_x = max_y = max_z = -math.inf

for line in lines:
    x, y, z, r = [int(x) for x in line.rstrip().replace("pos=<", "").replace(">", "").replace(" r=", "").split(",")]
    nanobots.append((r, x, y, z))

    min_x = min(x, min_x)
    min_y = min(y, min_y)
    min_z = min(z, min_z)
    max_x = max(x, max_x)
    max_y = max(y, max_y)
    max_z = max(z, max_z)

nanobots.sort(reverse=True)

min_x = min_y = min_z = 0 # we want to be close to the origin

print(nanobots)

max_distance, x, y, z = nanobots[0]

in_distance = list(filter(lambda nb: cityblock((x, y, z), (nb[1], nb[2], nb[3])) <= max_distance, nanobots))

print(in_distance)

print(len(in_distance))

# Part 2

def n_in_range(x, y, z):
    return len(list(filter(lambda nb: cityblock((x, y, z), (nb[1], nb[2], nb[3])) <= nb[0], nanobots)))

N = 1000
n_survivors = 100
n_mutations = 100
n_children = 0
generations = 1000

# TODO: beter to go over boundaries?
genepool = [(np.random.randint(min_x, max_x), np.random.randint(min_y, max_y), np.random.randint(min_y, max_y)) for _ in range(N)]

genepool[0] = (56482458, 41033492, 20905516) # best from last run
for generation in range(generations):

    # use negative values, to sort both number in range and distance to origin from low to high
    scores_genepool = [(-n_in_range(x, y, z), cityblock((x, y, z), (0, 0, 0)), x, y, z) for x, y, z in genepool]
    scores_genepool.sort()

    # next gen
    genepool = []
    for i in range(n_survivors):
        n, d, x, y, z = scores_genepool[i]
        genepool.append((x, y, z))

    # improve best solution
    n, d, x, y, z = scores_genepool[0]
    while -n_in_range(x - 1, y, z) <= n:
        x -= 1000
    while -n_in_range(x, y - 1, z) <= n:
        y -= 1000
    while -n_in_range(x, y, z - 1) <= n:
        z -= 1000
    genepool.append((x, y, z))

    for i in range(n_mutations):
        n, d, x, y, z = scores_genepool[i]
        # small mutations
        x = x + np.random.randint(0, 20001) - 10000
        y = y + np.random.randint(0, 20001) - 10000
        z = z + np.random.randint(0, 20001) - 10000
        genepool.append((x, y, z))

    for i in range(n_children):
        parent1 = np.random.randint(0, n_survivors)
        parent2 = np.random.randint(0, n_survivors)
        n1, d1, x1, y1, z1 = scores_genepool[parent1]
        n2, d2, x2, y2, z2 = scores_genepool[parent1]
        x, y, z = (x1 + x2) // 2, (y1 + y2) // 2, (z1 + z2) // 2


    # mutations
    for i in range(N - n_survivors - n_children):
        genepool.append((np.random.randint(min_x, max_x), np.random.randint(min_y, max_y), np.random.randint(min_y, max_y)))

    print(scores_genepool[0])

# problem not good for genetic alg, bin search would have been better

# 868, 121894826 => too high
# 906, 116781977 => too high

# (-868, 121894826, 57372805, 42394991, 22127030)
# (-877, 118592173, 56522885, 41043532, 21025756)
# (-906, 116781977, 55874314, 40470929, 20436734)
# (-975, 113799398, 55551180, 38979642, 19268576)