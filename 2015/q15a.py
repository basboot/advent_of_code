# PROBLEM IS NON LINEAR!

from collections import defaultdict

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *


file1 = open('q15a.txt', 'r')
lines = file1.readlines()

m = Model()

DECISION_VAR, NAME, CAPACITY, DURABILITY, FLAVOR, TEXTURE, CALORIES = 0, 1, 2, 3,4 , 5, 6


ingredients = []
for line in lines:
    # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    name, _, capacity, _, durability, _, flavor, _, texture, _, calories = line.rstrip().replace(":", "").replace(",", "").split(" ")

    ingredients.append((m.add_var(var_type=INTEGER), name, int(capacity), int(durability), int(flavor), int(texture), int(calories)))

print(ingredients)

# exactly 100 ts
m += xsum(ingredients[i][DECISION_VAR] for i in range(len(ingredients))) == 100


objective = 0
for property in [CAPACITY, DURABILITY, FLAVOR, TEXTURE]:
    # sum instead of xsum for max
    objective *= xsum(ingredients[i][DECISION_VAR] * ingredients[i][property] for i in range(len(ingredients)))

m.objective = maximize(objective)

print("-----------------------")
print(m.objective)


m.max_gap = 0.05
status = m.optimize(max_seconds=300)
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for i in range(len(ingredients)):
       print(f"{ingredients[i][NAME]} = {ingredients[i][DECISION_VAR]}")