import heapq
import math
from functools import cache
from itertools import product

from sympy import Symbol, solve
import numpy as np

file1 = open('q23a.txt', 'r')
file_lines = file1.readlines()

amphipods = []

SETTINGS = {
    1: [2, 1],
    2: [4, 10],
    3: [6, 100],
    4: [8, 1000]
}

DESTINATION, ENERGY = 0, 1

INITIAL = 0
BURROW = INITIAL + 4 * 2
GOAL = BURROW + 11 # don't need al, but will make calculations easier I hope

initial_state = [0] * (8 + 11 + 8)

for i in range(2):
    situation = file_lines[2 + i].rstrip()
    for pos in range(len(situation)):
        if situation[pos] in ['A', 'B', 'C', 'D']:
            amphipods.append((ord(situation[pos]) - ord('A') + 1, 1 - i, pos - 1)) # 0 is bottom, pos is up
            initial_state[(pos - 3) + (1 - i)] = ord(situation[pos]) - ord('A') + 1

print(amphipods)

initial_state = tuple(initial_state)

goal_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4)

# initial_state = (1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 3, 3, 4, 4)

# initial_state = (1, 2, 4, 3, 3, 0, 1, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
print(initial_state)

print("----------")

# exit()

# move initial amphipods to end state if they are already in place

new_initial_state = list(initial_state)

for i in range(0, 8, 2):
    amphipod2 = initial_state[i + 0]
    amphipod1 = initial_state[i + 1]

    desired = (i // 2) + 1

    if amphipod1 == amphipod2 and amphipod1 == desired:
        # move
        new_initial_state[i + BURROW + 11 + 1] = amphipod1
        new_initial_state[i + 1] = 0

    if amphipod2 == desired:
        new_initial_state[i + BURROW + 11 + 0] = amphipod2
        new_initial_state[i + 0] = 0


initial_state = tuple(new_initial_state)

print(initial_state)



UNREACHABLE = {2, 4, 6, 8}

@cache
def get_reachable_places(pos, state):
    reachable = []

    steps = 0
    for i in range(pos, 11):
        steps += 1
        if i in UNREACHABLE: # in front of hallway
            continue
        if state[i + BURROW] > 0: # obstruction
            break
        reachable.append((i + BURROW, steps))

    steps = 0
    for i in range(pos, - 1, -1):
        steps += 1
        if i in UNREACHABLE:  # in front of hallway
            continue
        if state[i + BURROW] > 0:  # obstruction
            break
        reachable.append((i + BURROW, steps))

    return reachable


@cache
def get_next_states(state):
    states = []

    # from initial state to burrow
    for i in range(8):
        amphipod_type = state[i]
        if amphipod_type == 0: # empty
            continue
        steps = 0
        if i % 2 == 0: # has to travel extra step (and must have free space above)
            if state[i + 1] > 0:
                continue
            else:
                steps += 1
        for new_index, extra_steps in get_reachable_places((i // 2) * 2 + 2, state):
            new_state = list(state) # copy and make mutable
            new_state[new_index] = new_state[i]
            new_state[i] = 0
            states.append((tuple(new_state), (steps + extra_steps) * SETTINGS[amphipod_type][ENERGY]))

    # from burrow to destination
    for i in range(11):
        amphipod_type = state[BURROW + i]
        if amphipod_type == 0:  # empty
            continue

        # TODO: check
        # everyone needs to have left before going to the goal
        if state[2 * (amphipod_type - 1)] > 0 or state[2 * (amphipod_type - 1) + 1] > 0:
            continue

        # path free? # TODO: faster to put after goal empty?
        from_pos = i + BURROW
        to_pos = (amphipod_type - 1) * 2 + 2 + BURROW
        # reverse if not in right order
        if from_pos > to_pos:
            from_pos, to_pos = to_pos, from_pos

        # TODO: this is wrong when reversed
        if sum(state[from_pos:to_pos + 1]) > amphipod_type: # obstruction because there must be someone else in the way
            continue

        steps = to_pos - from_pos

        # both empty? go to last
        if state[GOAL + 2 * (amphipod_type - 1)] == 0 and state[GOAL + 2 * (amphipod_type - 1) + 1] == 0:
            new_state = list(state) # copy and make mutable
            new_state[GOAL + 2 * (amphipod_type - 1)] = new_state[i + BURROW]
            new_state[i + BURROW] = 0
            states.append((tuple(new_state), (steps + 2) * SETTINGS[amphipod_type][ENERGY]))
        else:
            # second empty, and first has same amphipond? go to second
            if state[GOAL + 2 * (amphipod_type - 1)] == amphipod_type and state[GOAL + 2 * (amphipod_type - 1) + 1] == 0:
                new_state = list(state)  # copy and make mutable
                new_state[GOAL + 2 * (amphipod_type - 1) + 1] = new_state[i + BURROW]
                new_state[i + BURROW] = 0
                states.append((tuple(new_state), (steps + 1) * SETTINGS[amphipod_type][ENERGY]))

    return states


def heuristic(state):
    return 0
def a_star(start, goal):
    explored = set()
    to_explore = [] # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (heuristic(start), 0, start))

    while len(to_explore) > 0:
        estimated_cost, cost_so_far, state = heapq.heappop(to_explore)

        print(estimated_cost)

        if state in explored:
            continue
        explored.add(state)
        print(state)
        if state == goal:
            print("FOUND")
            return cost_so_far

        if state == (1, 0, 4, 0, 3, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0):
            print("reached strange state")

        actions = get_next_states(state)
        for next_state, next_cost in actions:
            print("NEXT:", next_state)
            if next_state in explored: # don't explore again
                continue

            # print("A", next_state, next_cost)

            heapq.heappush(to_explore, (heuristic(next_state) + cost_so_far + next_cost, next_cost + cost_so_far, next_state))
            # explored.add(next_state)
    return "Not found"


print(">>", a_star(initial_state, goal_state))
#
# for state, cost in get_next_states(initial_state):
#     print(state[0:8], state[8:8+11], state[8+11:], cost, state)


# NEXT: (1, 0, 4, 0, 3, 0, 1, 0, 4, 0, 0, 0, 0, 0, 0, 2, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0)
# NEXT: (1, 0, 4, 0, 3, 0, 1, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0)
# NEXT: (1, 0, 4, 0, 3, 0, 1, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0)
# NEXT: (1, 0, 4, 0, 3, 0, 1, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0)


