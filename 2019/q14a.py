import math
from itertools import permutations

import numpy as np

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

def split_amount_product(result):
    return [int(x) if x.isnumeric() else x for x in result.split(" ")]

recipes = {}
for line in lines:
    ingredients, result = line.rstrip().split(" => ")
    amount, product = split_amount_product(result)

    recipes[product] = {
        "amount": amount,
        "ingredients": [split_amount_product(ingredient) for ingredient in ingredients.split(", ")]
    }

spare = {}

def from_spare(amount, product):
    global spare

    if product in spare:
        if spare[product] >= amount:
            spare[product] -= amount
            return amount
        else:
            left = spare[product]
            spare[product] = 0
            return left
    else:
        return 0

def to_spare(product):
    global needed
    global spare

    recipe = recipes[product]
    #     = {
    #     "amount": amount,
    #     "ingredients": [split_amount_product(ingredient) for ingredient in ingredients.split(", ")]
    # }
    if product not in spare:
        spare[product] = recipe["amount"]
    else:
        spare[product] += recipe["amount"]

    for amount, ingredient in recipe["ingredients"]:
        if ingredient not in needed:
            needed[ingredient] = amount
        else:
            needed[ingredient] += amount




needed = {
    "FUEL": 1
}

while True:
    needed_products = list(needed.keys())
    assert len(needed_products) > 0, "Something went wrong, we do not need anything"
    product = needed_products[0]
    if product == "ORE":
        if len(needed_products) == 1:
            # ready
            break
        else:
            # take second
            product = needed_products[1]


    # get spare
    supply = from_spare(needed[product], product)
    needed[product] -= supply

    # check if spare was enough, else produce more spare
    if needed[product] > 0:
        to_spare(product)
    else:
        del needed[product]



print(spare)
print(needed)



