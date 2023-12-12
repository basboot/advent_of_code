# Using readlines()
import math

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

# start of spring, spring length, array #.?
def is_legal(pos, spring, unknown):
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

# find lower and upper bound to fit a spring (left to right), starting from pos
def find_fits(pos, spring, unknown):
    first_legal = None
    last_legal = None

    # print("ff", pos, spring, unknown)

    # find until where this spring can be fitted
    for pos in range(pos, len(unknown)):
        if is_legal(pos, spring, unknown):
            if first_legal is None:
                first_legal = pos
            last_legal = pos + spring - 1
        else:
            # break after it fits, but does not fit anymore
            if first_legal is not None:
                break

    assert first_legal is not None and last_legal is not None, "assumption that all springs fit does not hold"

    return first_legal, last_legal
#
# def break_puzzle(unknown, known):
#     unknowns = []
#     knowns = []
#
#     start_search = 0
#     upper_bound = len(unknown) - 1
#     spring_id = 0
#
#     start_spring = 0
#     start_unknown = 0
#
#     while spring_id < len(known):
#         spring = known[spring_id]
#
#         # print(f"spring {spring}")
#
#         first_pos, last_pos = find_fit(start_search, spring, unknown)
#
#         # print(f"{spring} fits {first_pos} - {last_pos}")
#
#         if last_pos < upper_bound:
#             upper_bound = last_pos
#
#         start_search = first_pos + spring + 1 # +1, because we need an empty spot behind the spring
#
#         # print(start_search, upper_bound)
#
#         spring_id += 1
#
#         # break
#         if start_search > upper_bound:
#
#             # print(f"break {start_spring} to {spring_id - 1}")
#             # print(f"{unknown[start_unknown:start_search]}")
#             new_unknown = unknown[start_unknown:start_search]
#             new_unknown[-1] = "." # we know this must be an empty space
#             unknowns.append(new_unknown)
#             # print(f"{known[start_spring:spring_id]}")
#             knowns.append(known[start_spring:spring_id])
#             upper_bound = math.inf
#             start_spring = spring_id
#             start_unknown = start_search
#
#             # print(f"SU {start_unknown}, with {start_spring}")
#
#     # if not all springs have been fitted, add them
#     if len(known[start_spring:]) > 0:
#         unknowns.append(unknown[start_unknown:])
#         knowns.append(known[start_spring:])
#
#     return unknowns, knowns



def is_legal_arrangement(current_arrangement, known, complete=False):
    arrangement = analyse_arrangement(current_arrangement)

    if complete:
        return arrangement == known
    else:
        return arrangement == known[:len(arrangement)]

def create_legal_arrangements(current_arrangement, unknown, known, depth, legal_arrangements):
    # check solution if we reach the end
    if depth == len(unknown):
        if is_legal_arrangement(current_arrangement, known, True):
            legal_arrangements.append(current_arrangement)
        return

    # backtrack on illegal arrangements
    if unknown[depth] == ".":
        if not is_legal_arrangement(current_arrangement, known):
            return

    # known characters can always be added
    if unknown[depth] in [".", "#"]:
        create_legal_arrangements(current_arrangement + [unknown[depth]], unknown, known, depth + 1, legal_arrangements)
    else:
        assert unknown[depth] == "?", f"Illegal char in unknown arrangement {unknown[depth]}"

        # try both options for ?
        for spring_option in [".", "#"]:
            create_legal_arrangements(current_arrangement + [spring_option], unknown, known, depth + 1, legal_arrangements)


def replace_only_fit(unknown, known):
    for i in range(len(known)):
        spring = known[i]

        count = 0

        # print("------", spring)

        for pos in range(len(unknown)):
            if is_legal(pos, spring, unknown):
                count += 1
        if count == 1:
            print("FOUND")

print(replace_only_fit(['?', '?', '.', '.', '#', '#', '#', ".", "?"], [1, 1, 3]))

# for unknown, known in springs:
#     partial_unknowns, partial_knowns = break_puzzle(unknown, known)

# legal_arrangements = []

# for unknown, known in springs:
#     create_legal_arrangements([], unknown, known, 0, legal_arrangements)
# print("Part 1", len(legal_arrangements))

# print(springs[0][0], springs[0][1])
# print(break_puzzle(['?', '?', '?', '.', '#', '#', '#', "?", "?"], springs[0][1]))

# total = 0
# for unknown, known in springs:
#     partial_unknowns, partial_knowns = break_puzzle(unknown, known)
#
#     print("---------")
#     print(unknown, known)
#
#     n_arrangements = 1
#     for i in range(len(partial_unknowns)):
#         legal_arrangements = []
#         create_legal_arrangements([], partial_unknowns[i], partial_knowns[i], 0, legal_arrangements)
#         n_arrangements *= len(legal_arrangements)
#
#         print(partial_unknowns[i], partial_knowns[i])
#         print(len(legal_arrangements))
#
#     print("-", n_arrangements)
#
#     break
#     total += n_arrangements
#
#
#
# print("Part 1", total)