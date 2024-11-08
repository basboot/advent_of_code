file1 = open('q21a.txt', 'r')
lines = file1.readlines()

allergen_mappings = {}
all_ingredients = set()
all_ingredients_list = []

for line in lines:
    ingredients, allergens = line.rstrip().replace(")", "").replace("contains ", "").split(" (")
    ingredients = set(ingredients.split(" "))
    allergens = allergens.split(", ")
    #
    # print(ingredients)
    # print(allergens)

    all_ingredients = all_ingredients.union(ingredients)
    all_ingredients_list += list(ingredients)

    for allergen in allergens:
        # allergen could be in all ingredients
        if allergen in allergen_mappings:
            allergen_mappings[allergen] = allergen_mappings[allergen].intersection(ingredients)
        else:
            # allergen must be in the intersection of the two ingredient lists
            allergen_mappings[allergen] = ingredients

# print(allergen_mappings)

# use uniqueness to clean up mappings
change = True
while change:
    change = False
    for allergen in allergen_mappings:
        # if unique
        if len(allergen_mappings[allergen]) == 1:
            # clean up all others
            ingredient = list(allergen_mappings[allergen])[0] # the known ingredient/allergen mapping
            for other_allergen in allergen_mappings:
                if other_allergen == allergen:
                    continue # skip self
                if ingredient in allergen_mappings[other_allergen]:
                    allergen_mappings[other_allergen].remove(ingredient)
                    change = True

print(allergen_mappings)

allergen_ingredients = set()
for allergen in allergen_mappings:
    allergen_ingredients = allergen_ingredients.union(allergen_mappings[allergen])


non_allergen_ingredients = all_ingredients - allergen_ingredients
print(non_allergen_ingredients)

total = 0
for ingredient in all_ingredients_list:
    if ingredient in non_allergen_ingredients:
        total += 1

print("Part 1", total)

sorted_allergens = list(allergen_mappings.keys())
sorted_allergens.sort()

sorted_ingredients = []
for allergen in sorted_allergens:
    sorted_ingredients.append(list(allergen_mappings[allergen])[0])
print("Part 2", ",".join(sorted_ingredients))

