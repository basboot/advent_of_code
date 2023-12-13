# Using readlines()
import math
import time

file1 = open('q12a.txt', 'r')
lines = file1.readlines()
from ast import literal_eval

# operational (.) or damaged (#) or ?

max_spring_length = -math.inf

springs = []
for line in lines:
    unknown, known = list(line.rstrip().split(" ")[0]), literal_eval("[" + line.rstrip().split(" ")[1] + "]")

    print(line)

    max_spring_length = max(max_spring_length, max(known))

    unknown = list("?".join(["".join(unknown)]*5))
    known = known * 5

    print(unknown, known)


    springs.append((unknown, known))


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
        constraints.append(set(constraint))

    return constraints

def split_unknown(unknown):
    unknowns = []
    new_unknown = []
    for char in unknown:
        if char == ".":
            if len(new_unknown) > 0:
                unknowns.append(new_unknown)
                new_unknown = []
        else:
            new_unknown.append(char)

    if len(new_unknown) > 0:
        unknowns.append(new_unknown)
    return unknowns




# legal_arrangements = 0
# def count_legal_arrangements(constraints, known, depth, sum_known, sum_used):
#     global legal_arrangements
#     if depth == len(constraints): # at end
#         if len(known) == 0: # and everything used
#             legal_arrangements += 1
#         #     print(solution)
#         # else:
#         #     print("end reached without solution: ", solution)
#         return
#
#     # break early when not feasible
#     if sum_known - sum_used > len(constraints) - depth:
#         return
#
#     # use config, or use 0
#     if len(known) > 0:
#         options = [0, known[0]]
#     else:
#         options = [0]
#
#     for option in options:
#         # print(f"try {option} at depth {depth}")
#         # print(">>>", depth, constraints)
#         if option in constraints[depth]: # TODO + 1
#             count_legal_arrangements(constraints, known if option == 0 else known[1:], min(len(constraints), depth + option + 1), sum_known, sum_used + option)
#


def count_legal_arrangements_with_remainder(constraints, known, depth, remainders, sum_remainders, sum_room_left, last_part, multiplier=1):
    # print(last_part)
    # global legal_arrangements
    if depth == len(constraints): # at end
        # TODO: check if there is no remainder => empty tuples () are also keys :-)

        remainder = tuple(known)

        if remainder in remainders:
            remainders[remainder] += multiplier
        else:
            remainders[remainder] = multiplier
        return

    # breaking early only possible on last part
    # break early when not feasible
    if last_part and sum_remainders > sum_room_left:
        pass
        return

    # use config, or use 0
    if len(known) > 0:
        options = [0, known[0]]
    else:
        options = [0]

    for option in options:
        # print(f"try {option} at depth {depth}")
        # print(">>>", depth, constraints)
        if option in constraints[depth]: # TODO + 1
            count_legal_arrangements_with_remainder(constraints, known if option == 0 else known[1:], min(len(constraints), depth + option + 1),
                                                    remainders, sum_remainders - option, sum_room_left - option - 1, last_part, multiplier)



total = 0
print(springs)
i = 0
for unknown, known in springs:
    i += 1
    print("spring: ", i)

    unknown_splits = split_unknown(unknown) # split unknowns at dots

    # print(unknown)
    # print(unknown_splits)
    # print("----")
    # exit()
    current_solution = {tuple(known): 1} # start solution is full knowns, 1 time (=multiplier)

    new_remainders = {} # laat deze berekenen voor de current solutions
    # print("start", current_solution)

    for j in range(len(unknown_splits)):
        unknown_split = unknown_splits[j]
        last_part = j == len(unknown_splits) - 1
        constraints = create_constraints(unknown_split)
        # print("-----")
        # print("C S", constraints, unknown_split)

        remainders = {}  # tel alles uit new remainders hierin op => en vervang current solution als klaar

        # for every solution so far, see if we can find a sequel
        for known_remainder in current_solution:
            count_legal_arrangements_with_remainder(constraints, known_remainder, 0, remainders,
                                                    sum(known_remainder), len(constraints), last_part,
                                                    current_solution[known_remainder])
        # print(remainders)
        current_solution = remainders # replace current solution with new remainders and move to next split

    # print(current_solution)
    # print(current_solution[()])


    total += current_solution[()]

    print(">>> %s seconds and counting" % (time.time() - start_time))

print("Part 2", total)

print("--- %s seconds ---" % (time.time() - start_time))

# --- 0.07763504981994629 seconds ---
