# Using readlines()
import math
import time
from functools import cache

file1 = open('q12a.txt', 'r')
lines = file1.readlines()
from ast import literal_eval

# operational (.) or damaged (#) or ?

max_spring_length = -math.inf

springs = []
for line in lines:
    unknown, known = list(line.rstrip().split(" ")[0]), literal_eval("[" + line.rstrip().split(" ")[1] + "]")


    unknown = list("?".join(["".join(unknown)]*5))
    known = known * 5

    springs.append((unknown, known))

    max_spring_length = max(max_spring_length, max(known))


start_time = time.time()

# start of spring, spring length, array #.?
def is_legal(pos, spring, unknown):
    if spring == 0:
        if unknown[pos] == "?" or unknown[pos] ==".":
            return True

    # can position before be .
    if pos > 0 and unknown[pos - 1] == "#":
        return False

    # does spring fit?
    if pos + spring > len(unknown):
        return False

    # can position after be .
    if pos + spring < len(unknown) and unknown[pos + spring] == "#":
        return False

    # can spring positions be #
    for i in range(pos, pos + spring):
        if unknown[i] == ".":
            return False

    # everything is ok :-)
    return True

def create_constraints(unknown):
    constraints = []
    for pos in range(len(unknown)):
        constraint = []
        # find all spring length that can be used at this position
        for i in range(max_spring_length + 1):
            if (is_legal(pos, i, unknown)):
                constraint.append(i)
        constraints.append(tuple(constraint))

    return constraints



# changed to returning the count instead of updating globals + used tuples and removed depth for caching
@cache
def count_legal_arrangements(remaining_constraints, known):
    if len(remaining_constraints) == 0: # at end
        if len(known) == 0: # and everything used
            return 1
        return 0

    # use config, or use 0
    if len(known) > 0:
        options = [0, known[0]]
    else:
        options = [0]

    legal_arrangements = 0
    for option in options:
        # print(f"try {option} at depth {depth}")
        # print(">>>", depth, constraints)
        if option in remaining_constraints[0]: # TODO + 1
            legal_arrangements += count_legal_arrangements(remaining_constraints[option + 1:], known if option == 0 else known[1:])

    return legal_arrangements


total = 0


for unknown, known in springs:
    legal_arrangements = 0
    constraints = create_constraints(unknown)
    total += count_legal_arrangements(tuple(constraints), tuple(known))


print("Part 1", total)

print("--- %s seconds ---" % (time.time() - start_time))

# --- 0.07763504981994629 seconds ---