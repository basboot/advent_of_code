store_ranges = True
fresh_ranges = []
fresh_range_first_last_values = []

def is_fresh(n):
    for first, last in fresh_ranges:
        if first <= n <= last:
            return True
    return False

total = 0

with open("q5a.txt") as f:
    for line in f:
        if line.strip() == "":
            store_ranges = False
            continue

        if store_ranges:
            first, last = tuple(map(int, line.strip().split("-")))
            fresh_ranges.append((first, last))
            fresh_range_first_last_values.append((first, "FIRST"))
            fresh_range_first_last_values.append((last, "LAST"))
        else:

            ingredient_id = int(line.strip())

            if is_fresh(ingredient_id):
                total += 1


fresh_range_first_last_values.sort()

max_fresh = 0
in_ranges = 0
first = 0
for ingredient_id, first_last in fresh_range_first_last_values:
    if first_last == "FIRST":
        if in_ranges == 0:
            first = ingredient_id
        in_ranges += 1
    else: # LAST
        if in_ranges == 1:
            max_fresh += (ingredient_id - first) + 1
        in_ranges -= 1



print(f"Part 1: {total}")
print(f"Part 2: {max_fresh}")