from collections import defaultdict

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *


file1 = open('q15a.txt', 'r')
lines = file1.readlines()

NAME, CAPACITY, DURABILITY, FLAVOR, TEXTURE, CALORIES = 0, 1, 2, 3,4 , 5

N = 1000
n_survivors = 100
n_children = 600
generations = 1000

ingredients = []
for line in lines:
    # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    name, _, capacity, _, durability, _, flavor, _, texture, _, calories = line.rstrip().replace(":", "").replace(",", "").split(" ")

    ingredients.append((int(capacity), int(durability), int(flavor), int(texture), int(calories))) # name,

properties = np.array(ingredients)

genepool = np.random.multinomial(100, [1/len(ingredients)]*len(ingredients), size=N)

# print(genepool)

for generation in range(generations):

    values = np.matmul(genepool, properties)

    # Part 1
    #values[:,4] = 1 # set calories to 1 to remove from product

    # Part 2
    values[:, 4] = (values[:, 4] == 500)  # only keep 500 calories


    values[values < 0] = 0 # set negatove values to zero


    scores = np.prod(values, 1)

    # print(scores)

    score_indices = np.argsort(scores)[::-1]

    # print(score_indices)
    # print(scores[score_indices])

    genepool = genepool[score_indices] # put genepool in score order

    print(f"Gen #{generation} Best", scores[score_indices[0]])

    for i in range(n_children):
        parent1 = genepool[np.random.randint(0, n_survivors)]
        parent2 = genepool[np.random.randint(0, n_survivors)]

        child = (parent1 + parent2) // 2

        child[0] += 100 - sum(child) # fix integer/rounding errors

        genepool[n_survivors + i] = child # put child in genepool

    # add mutations

    genepool[n_survivors + n_children:] = np.random.multinomial(100, [1/len(ingredients)]*len(ingredients), size=N - n_survivors - n_children)




