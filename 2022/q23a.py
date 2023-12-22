# Using readlines()
from tools.advent_tools import *

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

elves, width, height = read_grid(lines, GRID_SET, lambda a: a.strip(), {".": None, "#": "elve"})

# print(f"{len(elves)} elves found")

def show_elves():
    for i in range(height):
        for j in range(width):
            print("#" if (i, j) in elves else ".", end="")
        print()


NSWE = [
    [7, 0, 1], # N
    [3, 4, 5], # S
    [5, 6, 7], # W
    [1, 2, 3], # E
]

#               0N      1NE      2E     3SE      4S      5SW       6W       7NW
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# print(elves)

# Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions
start_direction = 0

def move_elves(start_direction):
    propositions = {}
    # each Elf considers the eight positions adjacent to themself
    for elve in elves:
        i, j = elve

        # ach Elf considers the eight positions adjacent to themself
        occupied = [1 if (i + di, j + dj) in elves else 0 for di, dj in DIRECTIONS]

        # If no other Elves are in one of those eight positions, the Elf does not do anything
        if sum(occupied) == 0:
            continue


        # Otherwise, the Elf looks in each of four directions
        for d in range(4):
            # get three options (eg NE, N, NW)
            direction_ids = NSWE[(d + start_direction) % 4]
            # middle option is where the elve itself wants to go
            proposition = (i + DIRECTIONS[direction_ids[1]][0], j + DIRECTIONS[direction_ids[1]][1])

            if sum([1 if (i + DIRECTIONS[direction_id][0], j + DIRECTIONS[direction_id][1]) in elves else 0 for direction_id in direction_ids]) == 0:
                if proposition in propositions:
                    propositions[proposition].append(elve)
                else:
                    propositions[proposition] = [elve]
                break # no more than one proposition

    # After each Elf has had a chance to propose a move, the second half of the round can begin.
    # Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose
    # moving to that position. If two or more Elves propose moving to the same position, none of those Elves move.




    for proposition in propositions:
        if len(propositions[proposition]) > 1:
            continue # more than one, so don't move
        else:
            # remove elve from previous
            # print(elves)
            # print(f"{propositions[proposition][0]} -> {proposition}")
            elves.remove(propositions[proposition][0])
            # and place at new
            elves.add(proposition)

    return len(propositions)



# # Part 1
# for i in range(100):
#     # print("Round", i + 1)
#     n = move_elves(i % 4)
#
#     if i + 1 == 10:
#         break
#
# i_s = [i for i, j in elves]
# j_s = [j for i, j in elves]
#
# print("Part 1", (max(i_s) - min(i_s) + 1) * (max(j_s) - min(j_s) + 1) - len(elves))


# Part 2
i = 0
while True:
    n = move_elves(i % 4)

    if n == 0:
        break

    i += 1

print("Part 2", i + 1)


