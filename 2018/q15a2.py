import functools
import math
from collections import Counter, deque
from dataclasses import dataclass
from functools import cache, reduce

import numpy as np
import matplotlib.pyplot as plt

file1 = open('q15a.txt', 'r')

import heapq
from collections import defaultdict

walls = set()

@dataclass
class Unit:
    id: int
    power: int
    hp: int
    i: int
    j: int
    type: str


units = {}
elves = {} # double bookkeeping for locations of live elves and units only
goblins = {}

ELF_POWER = 40 # Part 2

id = 0
for i, line in enumerate(file1):
    for j, cell in enumerate(line.rstrip()):

        match cell:
            case ".":
                pass
            case "#":
                walls.add((i, j))
            case "G" | "E":
                # sort keys to get correct order
                if cell == "E":
                    units[id] = Unit(id, ELF_POWER, 200, i, j, cell)
                    elves[(i, j)] = units[id]
                else:
                    units[id] = Unit(id, 3, 200, i, j, cell)
                    goblins[(i, j)] = units[id]

                id += 1

def show_map(max_size):
    for i in range(max_size):
        summary = "   "
        for j in range(max_size):
            if (i, j) in walls:
                print("#", end="")
                continue
            if (i, j) in elves:
                summary += f"{elves[(i, j)].type}({elves[(i, j)].hp}), "
                print(elves[(i, j)].type, end="")
                continue
            if (i, j) in goblins:
                summary += f"{goblins[(i, j)].type}({goblins[(i, j)].hp}), "
                print(goblins[(i, j)].type, end="")
                continue
            print(".", end="")
        print(summary)

round = 0
game_over = False
while not game_over:
    print(f"Round {round}:")
    if round == 23:
        print("debug round 23")
    round += 1
    show_map(32)

    # For instance, the order in which units take their turns within a round is the reading order of their starting
    # positions in that round, regardless of the type of unit or whether other units have moved after the round started.
    player_order = sorted(list(units.values()), key=lambda u: (u.i, u.j))

    print("order:")
    print([f"({p.i}, {p.j})" for p in player_order])

    full_round = True
    for i, player in enumerate(player_order):
        # Each unit begins its turn by identifying all possible targets (enemy units). If no targets remain, combat ends.
        # use goblins and elves
        print("** Player", player)

        # skip if dead
        if player.hp == 0:
            print("SKIP DEAD PLAYER")
            continue

        # need to check if round was fully played
        if game_over:
            full_round = False
            continue

        # Then, the unit identifies all of the open squares (.) that are in range of each target; these are the squares
        # which are adjacent (immediately up, down, left, or right) to any target and which aren't already occupied by a wall or
        # another unit. Alternatively, the unit might already be in range of a target. If the unit is not already in range of a target,
        # and there are no open squares which are in range of a target, the unit ends its turn.

        # find all enemies, and put all squares around them in a target list
        enemys = goblins if player.type == "E" else elves
        friends = goblins if player.type == "G" else elves

        def find_closest_locations(start_i, start_j, targets) -> list | None:
            visited = set()
            visited.add((start_i, start_j))
            to_explore = deque([(0, start_i, start_j, None, None)])

            solutions = []
            closest = math.inf

            unreachable = walls.union(elves).union(goblins) # TODO: check if this works

            while len(to_explore) > 0:
                cost, i, j, first_i, first_j = to_explore.popleft()

                if cost > closest:
                    return solutions  # all closest found, stop looking


                if (i, j) in targets:
                    if cost == 0:
                        return # enemy adjacent, stop looking
                    closest = cost
                    solutions.append((cost, i, j, first_i, first_j))


                for di, dj in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                    ni, nj = i + di, j + dj
                    if (ni, nj) in visited or (ni, nj) in unreachable: # dont visit twice, or go to unreachable places
                        continue

                    visited.add((ni, nj)) # Mark earlu as visited, to avoid exploring same route

                    to_explore.append((cost + 1, ni, nj, ni if first_i is None else first_i, nj if first_j is None else first_j))
                    # length, i-target, j-target, i-step, j-step

            return solutions # no solution found


        # 1. is one of them adjacent -> attack

        # allready in range
        in_range = False
        for di, dj in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
            ni, nj = player.i + di, player.j + dj
            if (ni, nj) in enemys:
                in_range = True
                print("Already in range of a target")

        # skip if in range
        if not in_range:
            target_locations = set()
            for enemy in enemys.values():
                for di, dj in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                    ni, nj = enemy.i + di, enemy.j + dj
                    if (ni, nj) in walls or (ni, nj) in elves or (ni, nj) in goblins:
                        continue  # not reachable
                    target_locations.add((ni, nj))

            print(target_locations)

            paths = find_closest_locations(player.i, player.j, target_locations)

            print(player)
            print(paths)

            if paths is not None and len(paths) > 0: # move needed
                paths.sort()

                # perform first move
                _, i, j, ni, nj = paths[0]
                del friends[(player.i, player.j)]

                player.i = ni
                player.j = nj
                friends[(ni, nj)] = player

                print(f"Move to ({ni}, {nj})")
                print(paths)
            else:
                print("No move found")

        # To attack, the unit first determines all of the targets that are in range of it by being immediately adjacent to it.
        # If there are no such targets, the unit ends its turn. Otherwise, the adjacent target with the fewest hit points is selected;
        # in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.

        targets = []

        for di, dj in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
            ni, nj = player.i + di, player.j + dj
            if (ni, nj) in enemys:
                targets.append((enemys[(ni, nj)].hp, ni, nj, enemys[(ni, nj)].id))
        if len(targets) > 0:
            targets.sort()
            # TODO: attack target[0]
            print("ATTACK")
            # The unit deals damage equal to its attack power to the selected target, reducing its hit points by that amount.
            # If this reduces its hit points to 0 or fewer, the selected target dies: its square becomes . and it
            # takes no further turns.
            _, _, _, unit_id = targets[0]
            enemy = units[unit_id]

            print(f"BEFORE ATTACK {player.id} -> {unit_id}")
            print(units)
            enemy.hp -= player.power
            print("AFTER")
            print(units)

            # enemy dead, remove
            if enemy.hp <= 0:
                enemy.hp = 0
                print(">>>> Enemy died: ", enemys[(enemy.i, enemy.j)])
                print(goblins)
                print(elves)
                del enemys[(enemy.i, enemy.j)]
                print("REMOVED")
                print(goblins)
                print(elves)



        if len(goblins) == 0 or len(elves) == 0:
            print("Game over")
            print(units)
            game_over = True


    print(f"Round {round}:")
    show_map(7)

print(full_round)
print(sum([u.hp for u in units.values()]) * (round - (1 if not full_round else 0)))

# 234444 - too high
# 225096

score = {
    "G": 0,
    "E": 0
}
for u in units.values():
    score[u.type] = score[u.type] + (1 if u.hp > 0 else 0)
print(score)
