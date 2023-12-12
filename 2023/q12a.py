# Using readlines()
import time

file1 = open('q12a.txt', 'r')
lines = file1.readlines()
from ast import literal_eval

# operational (.) or damaged (#) or ?

springs = []
for line in lines:
    unknown, known = list(line.rstrip().split(" ")[0]), literal_eval("[" + line.rstrip().split(" ")[1] + "]")
    springs.append((unknown, known))

# count neighbouring #
def analyse_arrangement(current_arrangement):
    arrangement = []
    hash_count = 0
    for spring in current_arrangement:
        match spring:
            case "#":
                hash_count += 1
            case ".":
                if hash_count > 0:
                    arrangement.append(hash_count)
                    hash_count = 0
            case _:
                assert True, "Arrangement can only contain # and ."

    if hash_count > 0:
        arrangement.append(hash_count)

    return arrangement

def is_legal_arrangement(current_arrangement, known, complete=False):
    if current_arrangement[-1] == 0:
        current_arrangement = current_arrangement[:len(current_arrangement) - 1]

    if complete:
        return current_arrangement == known
    else:
        return current_arrangement == known[:len(current_arrangement)]

def create_legal_arrangements(current_arrangement, unknown, known, depth, sum_known, sum_solution):
    global legal_arrangements
    # check solution if we reach the end
    if depth == len(unknown):
        if is_legal_arrangement(current_arrangement, known, True):
            legal_arrangements += 1
        return

    # break if we do not have enough room left
    # print(unknown, depth, known, current_arrangement)
    if len(unknown) - depth < sum_known - sum_solution:
        return

    # backtrack on illegal arrangements
    if unknown[depth] == ".":
        if not is_legal_arrangement(current_arrangement, known):
            return

    # known characters can always be added
    if unknown[depth] in [".", "#"]:
        new_arrangement = current_arrangement.copy()
        if unknown[depth] == "#":
            new_arrangement[-1] += 1
        else:
            if new_arrangement[-1] > 0:
                new_arrangement.append(0)

        create_legal_arrangements(new_arrangement, unknown, known, depth + 1, sum_known, sum_solution + (1 if unknown[depth] == "#" else 0))
    else:
        assert unknown[depth] == "?", f"Illegal char in unknown arrangement {unknown[depth]}"

        # try both options for ?
        for spring_option in [".", "#"]:
            new_arrangement = current_arrangement.copy()
            if spring_option == "#":
                new_arrangement[-1] += 1
            else:
                if new_arrangement[-1] > 0:
                    new_arrangement.append(0)

            create_legal_arrangements(new_arrangement, unknown, known, depth + 1, sum_known, sum_solution + (1 if spring_option == "#" else 0))



start_time = time.time()


legal_arrangements = 0
total = 0
for unknown, known in springs:
    legal_arrangements = 0
    create_legal_arrangements([0], unknown, known, 0, sum(known), 0)
    total += legal_arrangements

    # print("-", len(legal_arrangements))

print("Part 1", total)

print("--- %s seconds ---" % (time.time() - start_time))

# --- 1.7099559307098389 seconds ---
# --- 0.9779319763183594 seconds ---