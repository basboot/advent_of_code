# Using readlines()
import math
import time

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

import numpy as np

def show_platform(p):
    for i in range(len(p)):
        for j in range(len(p[0])):
            match p[i, j]:
                case 0:
                    print(".", end="")
                case 1:
                    print("O", end="")
                case 2:
                    print("#", end="")
        print()


platform = [] # 1 at [i, j], round rocks only!
rocks = [] # (i, j, type), all rocks + boundaries

NOTHING, ROUND, SQUARE, BOUNDARY = 0, 1, 2, 3
ROCK_TYPES = {".": NOTHING, "O": ROUND, "#":SQUARE, "X": BOUNDARY}
for i in range(len(lines)):
    input = list(lines[i].rstrip())

    row = []
    for j in range(len(input)):
        row.append(1 if input[j] == "O" else 0)
        # DEBUG (put 2's for immovable blocks, so we can print, don;t forget to remove when calculating the score!)
        # row.append(1 if input[j] == "O" else (2 if input[j] == "#" else 0))

        if input[j] != ".":
            rocks.append([i, j, ROCK_TYPES[input[j]]])
    platform.append(row)

platform = np.array(platform)

# Add immovable boundaries to prevent blocks falling 'out'
for i in range(-1, len(platform) + 1):
    rocks.append([i, -1, BOUNDARY])
    rocks.append([i, len(platform), BOUNDARY])
for j in range(-1, len(platform[0]) + 1):
    rocks.append([-1, j, BOUNDARY])
    rocks.append([len(platform[0]), j, BOUNDARY]) # there are double boundaries at corners but that should not be a problem

# sort rocks in falling direction (lowest pos first)
# return rocks, direction the blocks stack and the perpendicular axis (i_stack, j_stack, other_axis)
def north(rocks):
    rocks.sort(key=lambda rock: ((rock[1] + 1) << 8) | (rock[0] + 1)) # sort to getthem in the right order (+1 for neg values) by row first
    return rocks, 1, 0, 1
def south(rocks):
    rocks.sort(key=lambda rock: ((rock[1] + 1) << 8) | (rock[0] + 1), reverse=True) # sort to getthem in the right order (+1 for neg values) by row first
    return rocks, -1, 0, 1
def west(rocks):
    rocks.sort(key=lambda rock: ((rock[1] + 1)) | ((rock[0] + 1)) << 8) # sort to getthem in the right order (+1 for neg values) by row first
    return rocks, 0, 1, 0
def east(rocks):
    rocks.sort(key=lambda rock: ((rock[1] + 1)) | ((rock[0] + 1)) << 8, reverse=True) # sort to getthem in the right order (+1 for neg values) by row first
    return rocks, 0, -1, 0

def roll_blocks(rocks, f_rock_ordering):
    # roll blocks
    rocks, i_dir, j_dir, axis = f_rock_ordering(rocks)

    previous_block = (-math.inf, -math.inf, 10)
    for i in range(len(rocks)):
        # only move round blocks, in same row (fall until one above)
        if rocks[i][2] == ROUND and rocks[i][axis] == previous_block[axis]:
            new_i, new_j = previous_block[0] + i_dir, previous_block[1] + j_dir

            # update matrix
            platform[rocks[i][0], rocks[i][1]] = 0
            platform[new_i, new_j] = 1

            # update list
            rocks[i][0], rocks[i][1] = new_i, new_j #TODO: fix

        previous_block = rocks[i].copy()

    return rocks

# n, n-1,...,1 for calculating score
mp = np.transpose(np.array(range(len(platform), 0, -1)))

# Part 1
# rocks = roll_blocks(rocks, north)


# Part 2
def cycle(rocks):
    rocks = roll_blocks(rocks, north)
    rocks = roll_blocks(rocks, west)
    rocks = roll_blocks(rocks, south)
    rocks = roll_blocks(rocks, east)
    return rocks


start_time = time.time()
i = 0

WARM_UP = 100 # warm up cycles before comparison
MAX_CYCLES = 1000000000

while i < MAX_CYCLES:
    cycle(rocks)
    # if i % 10 == 0:
    #     print(f"{i} cycles, --- %s seconds and counting---" % (time.time() - start_time))

    if i == WARM_UP:
        platform_compare = platform.copy()
    # print(i)

    # compare after each cycle
    if i > WARM_UP and np.array_equal(platform, platform_compare):
        period = i - WARM_UP # calc repeating pattern
        skip_i = (((MAX_CYCLES - i) // period) - 1) * period # Go back one period, to prevent to go to far
        # print(">> period: ", period, "Now at:", i, "After skip: ", (i + skip_i))
        i += skip_i
    i += 1
    # print(f"After {i} = ", np.sum(mp * np.transpose(platform)))

print("--- %s seconds ---" % (time.time() - start_time))

# # Calculate and sum up
print("Part 2", np.sum(mp * np.transpose(platform)))

# 102505 too low ? 102505 too low!
# 102512 too high (gegokt uit cycle)
# andere opties in mijn cycles: 102509, 102507
