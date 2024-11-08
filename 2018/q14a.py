recipes = [int(x) for x in "37"]

elves = [0, 1]
print(recipes)

n_after = 293801
n_recipes = 10

while True:
    new_recipe = [int(x) for x in str(sum([recipes[x] for x in elves]))]

    recipes += new_recipe

    for i in range(len(elves)):
        elves[i] = (1 + elves[i] + recipes[elves[i]]) % len(recipes)

    if len(recipes) >= n_after + n_recipes:
        break

print("". join([str(x) for x in recipes[n_after:n_after + n_recipes]]))