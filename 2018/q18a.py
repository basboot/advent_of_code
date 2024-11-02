from collections import Counter
import numpy as np


file1 = open('q18a.txt', 'r')
lines = file1.readlines()

trees = set() # trees (|)
lumberyards = set() # lumberyard (#)

AREA = 0
for i, row in enumerate(lines):
    AREA = max(i, AREA)
    for j, cell in enumerate(row.rstrip()):
        if cell == "|":
            trees.add((i, j))
        if cell == "#":
            lumberyards.add((i, j))

def get_neighbours(pos):
    i, j = pos
    for di in [-1, 0, +1]:
        for dj in [-1, 0, +1]:
            if di == 0 and dj == 0:
                continue # skip self

            if i + di < 0 or i + di > AREA or j + dj < 0 or j + dj > AREA:
                continue # skip outside area

            yield (i + di, j + dj)


def show_area(trees, lumberyards):
    for i in range(AREA):
        for j in range(AREA):
            if (i, j) in trees:
                print("|", end="")
            else:
                if (i, j) in lumberyards:
                    print("#", end="")
                else:
                    print(".", end="")
        print()

iteration = 0

history = {}

fastforward = False
while iteration < 1000000000:
    # calculate neighbours
    neighbours = {}

    area_id = (frozenset(trees), frozenset(lumberyards))

    if not fastforward and area_id in history:
        print(f"seen this state before at iteration #{history[area_id] + 1}, now at #{iteration + 1}")

        period = iteration - history[area_id]
        iterations_left = (1000000000 - iteration - 1)
        periods_to_skip = iterations_left // period

        print(f"skipping {periods_to_skip * period} iterations")
        iteration += periods_to_skip * period

        fastforward = True


    history[area_id] = iteration

    for items_id, items in [("trees", trees), ("lumberyards", lumberyards)]:
        for item in items:
            for neighbour in get_neighbours(item):
                if neighbour not in neighbours:
                    neighbours[neighbour] = {
                        "trees": 0,
                        "lumberyards": 0  # TODO: look up defaultdict
                    }

                neighbours[neighbour][items_id] += 1

    # do update based on neighbours
    next_trees = set()
    next_lumberyards = set()

    for neighbour in neighbours:
        # An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
        if neighbour not in trees and neighbour not in lumberyards and neighbours[neighbour]["trees"] >= 3:
            next_trees.add(neighbour)

    for tree in trees:
        # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
        if tree in neighbours and neighbours[tree]["lumberyards"] >= 3:
            next_lumberyards.add(tree)
        else:
            next_trees.add(tree)

    for lumberyard in lumberyards:
        # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
        if lumberyard in neighbours and neighbours[lumberyard]["lumberyards"] >= 1 and neighbours[lumberyard]["trees"] >= 1:
            next_lumberyards.add(lumberyard)

    trees = next_trees
    lumberyards = next_lumberyards

    if iteration == 9:
        print("Part 1", len(trees) * len(lumberyards))

    iteration += 1

print("Part 2", len(trees) * len(lumberyards))


# 467819










