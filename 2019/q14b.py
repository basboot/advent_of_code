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


def from_spare(amount, product):
    global spare

    if product in spare:
        if spare[product] > amount:
            spare[product] -= amount
            return amount
        else:
            left = spare[product]
            spare[product] = 0
            del spare[product]
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




spare = {}

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

n_ore = 1000000000000

print("ORE needed for 1", needed["ORE"])
fuel_min = n_ore // needed["ORE"] - 50000
print("Produce at least", fuel_min)
ore_left = n_ore - (fuel_min * needed["ORE"])
print("Have ore left", n_ore - (fuel_min * needed["ORE"]))

print("SPARE before increase", spare)
# update spare
for product in spare:
    spare[product] *= fuel_min



#####
# spare = {}
# fuel_min = 0
# ore_left = n_ore
# print("SPARE before proceding", spare)


needed = {}

# 1510658317
print("START")
fuel = 0
while True:
    if fuel % 1000 == 0:
        print(fuel)
    needed["FUEL"] = 1
    # print("SPARE", spare)

    while True:
        # first check supply for all needed products
        needed_products = list(needed.keys())
        for product in needed_products:
            if product == "ORE":
                continue
            supply = from_spare(needed[product], product)
            needed[product] -= supply
            if needed[product] == 0:
                del needed[product]

        needed_products = list(needed.keys())
        if len(needed_products) == 0:
            break # we did not need anything, all came from spare products
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

    if "ORE" in needed:
        if needed["ORE"] > ore_left:
            break # stop, we couldn't produce the last ore
    fuel += 1

print("S", spare)
print("N", needed)
print(needed["ORE"])

print("Extra fuel", fuel)

print("Part 2, total fuel", (fuel_min + fuel))


# 452742