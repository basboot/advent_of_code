import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q21a.txt', 'r')
lines = file1.readlines()

image = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])


# tuple(map(tuple, arr))

def rule_to_matrix(rule):
    return np.array([[int(x) for x in r] for r in rule.replace(".", "0").replace("#", "1").split("/")])


rules = {}

# read rules
for line in lines:
    rule = line.rstrip().split(" => ")

    input = rule_to_matrix(rule[0])
    output = rule_to_matrix(rule[1])

    for i in range(4):
        rules[tuple(map(tuple, np.rot90(input, i)))] = output

    for i in range(4):
        rules[tuple(map(tuple, np.rot90(np.flip(input, 0), i)))] = output

    # a bit overkill... but dictionary will remove doubles
    for i in range(4):
        rules[tuple(map(tuple, np.rot90(np.flip(input, 1), i)))] = output


# enhance

for _ in range(18):
    if len(image) % 2 == 0:
        grid_size = 2
    else:
        if len(image) % 3 == 0:
            grid_size = 3
        else:
            assert True, "no multiple of 2 or 3"

    n_pixels = len(image) // grid_size

    new_image = np.zeros((n_pixels * (grid_size + 1), n_pixels * (grid_size + 1))) # increase size

    for i in range(n_pixels):
        for j in range(n_pixels):
            pixel = image[i * grid_size: (i + 1) * grid_size, j * grid_size: (j + 1) * grid_size]

            pixel_id = tuple(map(tuple, pixel))

            if pixel_id in rules:
                new_image[i * (grid_size + 1): (i + 1) * (grid_size + 1), j * (grid_size + 1): (j + 1) * (grid_size + 1)] = rules[pixel_id]

    image = new_image # replace image with enhanced version
    print(image)

print("Part 2", np.sum(image))