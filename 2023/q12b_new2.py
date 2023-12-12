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


def is_legal2(pos, spring, unknown):
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
def find_fits2(pos, spring, unknown):
    first_legal = None
    last_legal = None

    # print("ff", pos, spring, unknown)

    # find until where this spring can be fitted
    for pos in range(pos, len(unknown)):
        if is_legal2(pos, spring, unknown):
            if first_legal is None:
                first_legal = pos
            last_legal = pos + spring - 1
        else:
            # break after it fits, but does not fit anymore
            if first_legal is not None:
                break

    assert first_legal is not None and last_legal is not None, "assumption that all springs fit does not hold"

    return first_legal, last_legal

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

def find_fit(spring, unknown, pos=0, firstFit=False):
    first_legal = None
    last_legal = None

    # print("ff", pos, spring, unknown)

    # find until where this spring can be fitted
    for pos in range(pos, len(unknown)):
        if unknown[pos] == ".":
            continue
        if is_legal(pos, spring, unknown):
            # print(">>", pos, spring, unknown)
            return True
        else:
            if firstFit and unknown[pos] != "?":
                return False

    return False

def break_at_first_dot(unknown, known):
    # remove trailing dots
    unknown = unknown.copy()
    while unknown[0] == ".":
        unknown = unknown[1:]

    if "." not in unknown:
        return [unknown], [known], False

    first_dot = unknown.index(".")
    unknown1 = unknown[:first_dot]
    unknown2 = unknown[first_dot:]

    while len(unknown2) > 0 and unknown2[0] == ".":
        unknown2 = unknown2[1:]


    not_found = True
    from_left = 0
    for spring_id in range(len(known)):
        fit_left, fit_right = find_fit(known[spring_id], unknown1, from_left), find_fit(known[spring_id], unknown2, firstFit=True)
        # print(known[spring_id], fit_left, fit_right)

        # print(spring_id)
        # does fit left and fit right = give up
        if fit_left and fit_right:
            not_found = True
            break
        # does not fit left = found
        if not fit_left:
            # print("break")
            known1 = known[:spring_id]
            known2 = known[spring_id:]
            not_found = False
            break

        # does fit left, but does not fit right = keep searching
        from_left += (known[spring_id] + 1)

    # print(first_dot, unknown1, unknown2)
    # if not not_found:
    #     print(known1, known2)

    if not not_found:
        return [unknown1, unknown2], [known1, known2], True
    else:
        return [unknown], [known], False


def replace_only_fit(unknown, known):
    for i in range(len(known)):
        spring = known[i]

        count = 0

        # print("------", spring)

        for pos in range(len(unknown)):
            if is_legal2(pos, spring, unknown):
                count += 1
        if count == 1:
            print("FOUND")

#print(replace_only_fit(['?', '?', '.', '.', '#', '#', '#', ".", "?"], [1, 1, 3]))


# print(break_at_first_dot(['?', '.', '?', '#', '?', '?', '.', '.', '?', '?', '#', '.', '?', '.', '?', '?'], [1, 2]))
# exit()

# TODO: finish replace only fit
# TODO: repeat break at first dot (if possible)
# TODO: find other ways to break solutions into parts

legal_arrangements = 0
def divide_and_conquer(unknown, known):
    global legal_arrangements
    unknowns, knowns, broken = break_at_first_dot(unknown, known)
    # print(unknowns, knowns)

    legal_arrangements = 0
    create_legal_arrangements([0], unknown, known, 0, sum(known), 0)
    verify = legal_arrangements

    total = 1
    log = []
    for i in range(len(unknowns)):
        unknown, known = unknowns[i], knowns[i]
        legal_arrangements = 0
        create_legal_arrangements([0], unknown, known, 0, sum(known), 0)
        total *= legal_arrangements
        # a, b, c = len(legal_arrangements), unknown, known
        # log.append((a, b, c))

    # if verify != total:
    #     print(f"Incorrect")
    #     print("correct", verify, "incorrect", total)
    #     print(unknown, known)
    #     print(log)

    return total

start_time = time.time()

total = 0
for unknown, known in springs:
    # legal_arrangements = []
    # create_legal_arrangements([], unknown, known, 0, legal_arrangements, sum(known), 0)
    # total += len(legal_arrangements)

    total += divide_and_conquer(unknown, known)

    # print("-", len(legal_arrangements))

print("Part 2", total)

print("--- %s seconds ---" % (time.time() - start_time))

# van drie naar:
# --- 1.9364972114562988 seconds ---, 2x zo lang als zonder optimalisatie :-(

