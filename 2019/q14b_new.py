import math
from itertools import permutations

import numpy as np
import sympy

import cvxpy

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

def split_amount_product(result):
    return [int(x) if x.isnumeric() else x for x in result.split(" ")]

recipes = {}

symbols = {}

recipe_equations = []

for line in lines:
    ingredients, result = line.rstrip().split(" => ")
    amount, product = split_amount_product(result)

    recipes[product] = {
        "amount": amount,
        "ingredients": [split_amount_product(ingredient) for ingredient in ingredients.split(", ")]
    }


recipes_list = list(recipes.keys())

needed = {}

variables = {
    "ORE": cvxpy.Variable(integer=True)
}

constraints = [variables["ORE"] <= 1000000000000]

for i in range(len(recipes_list)):
    print(f"{recipes_list[i]} = {recipes[recipes_list[i]]['amount']} * r{i}")
    variables[recipes_list[i]] = cvxpy.Variable(integer=True)
    variables[f"r{i}"] = cvxpy.Variable(integer=True)

    constraints.append(variables[recipes_list[i]] == recipes[recipes_list[i]]['amount'] * variables[f"r{i}"])

    for amount, ingredient in recipes[recipes_list[i]]['ingredients']:
        if ingredient not in needed:
            needed[ingredient] = []
        needed[ingredient].append((f"r{i}", amount))

for ingredient, need in needed.items():
    value = 0
    print(f"{ingredient} >= {need}")
    for var, n in need:
        value += variables[var] * n
    constraints.append(variables[ingredient] >= value)

print("ORE <= 1000000000")


print("------")

print(constraints)

day_14b = cvxpy.Problem(cvxpy.Maximize(variables["FUEL"]), constraints)

print(day_14b.solve(solver=cvxpy.GLPK_MI))

# 34482758 too high
