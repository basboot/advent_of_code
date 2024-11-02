import math
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

recipes = [int(x) for x in "37"]

elves = [0, 1]
print(recipes)

n_after = "293801"
n_recipes = 0

LEN = len(n_after)

while True:
    new_recipe = [int(x) for x in str(sum([recipes[x] for x in elves]))]

    recipes += new_recipe

    for i in range(len(elves)):
        elves[i] = (1 + elves[i] + recipes[elves[i]]) % len(recipes)

    while n_recipes < len(recipes) - LEN:
        # print(n_recipes, len(recipes), recipes[n_recipes:n_recipes + 5], recipes)
        # print("". join([str(x) for x in recipes[n_recipes:n_recipes + 5]]))
        if "". join([str(x) for x in recipes[n_recipes:n_recipes + LEN]]) == n_after:
            print(n_recipes)
            exit()
        n_recipes += 1


