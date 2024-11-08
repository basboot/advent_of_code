import heapq

file1 = open('q23a.txt', 'r')
file_lines = file1.readlines()

amphipods = []

# TODO: convert type A to 0 etc, goal open closed not in global settings

START, MOVING, READY = 0, 1, 2

# TODO: rename
SETTINGS = {
    0: [3, 1],
    1: [5, 10],
    2: [7, 100],
    3: [9, 1000]
}

HALLWAY, ENERGY = 0, 1

BURROW_START = 1
BURROW_END = 11
burrow = set()

EMPTY = 4

TYPE, I, J, STATE = 0, 1, 2, 3

goals = (False, False, False, False)



for i in range(2):
    situation = file_lines[2 + i].rstrip()
    for pos in range(len(situation)):
        if situation[pos] in ['A', 'B', 'C', 'D']:
            amphipods.append((ord(situation[pos]) - ord('A'), 1 - i, pos, START)) # 0 is bottom, pos is up
            burrow.add((1 - i, pos))

def is_movable(amphipod, burrow, goals):
    # already in, no need to move
    if amphipod[STATE] == READY:
        return False
    # cannot go to desired goal
    if amphipod[STATE] == MOVING and not goals[amphipod[TYPE]]:
        return False
    # at bottom of hallway and someone standing in the way
    if amphipod[STATE] == START and amphipod[I] == 0 and (1, amphipod[J]) in burrow:
        return False

    return True

def free_spots(j_start, j_end, burrow):
    all_free = True
    reachable = []

    # print(f"check {j_start} to {j_end}")
    # print("range", j_start, j_end + 1 if j_end > j_start else -1, 1 if j_end > j_start else -1)

    cost = 0
    for j in range(j_start, j_end + (1 if j_end > j_start else -1), 1 if j_end > j_start else -1):
        # print(f"check {j}")
        cost += 1
        # not possible to block a hallway, also skip first (where we stand ourselves)
        if j in [3, 5, 7, 9] or j == j_start:
            continue
        if (2, j) not in burrow:
            reachable.append((j, cost - 1))
        else:
            # print(f"not reachable {j}: burrow {burrow}")
            all_free = False
            break
    return all_free, reachable


def heuristic(amphipods):
    estimated_cost = 0

    for amphipod in amphipods:
        if amphipod[STATE] == START:
            estimated_cost += (2 - amphipod[I]) * SETTINGS[amphipod[TYPE]][ENERGY]
        if amphipod[STATE] == MOVING:
            estimated_cost += (abs(amphipod[J] - SETTINGS[amphipod[TYPE]][HALLWAY]) + 1) * SETTINGS[amphipod[TYPE]][ENERGY]

    return estimated_cost




def get_actions(amphipods, burrow, goals, cost_to_go):
    actions = []
    for n in range(len(amphipods)):
        amphipod = amphipods[n]
        # print(amphipod)
        if not is_movable(amphipod, burrow, goals):
            # print(f"{amphipod} cannot move")
            continue
        else:
            # try to step into the burrow
            if amphipod[STATE] == START:
                # print(f"{amphipod} wants to go to the burrow")
                possible_js = free_spots(amphipod[J], BURROW_START, burrow)[1] + free_spots(amphipod[J], BURROW_END, burrow)[1]
                for next_j, cost in possible_js:
                    # cost in burrow + step outside hallway
                    # print(next_j, cost + 2 - amphipod[I])

                    next_burrow = burrow.copy()
                    next_amphipods = list(amphipods) # copy, and make mutable

                    type, ai, aj, state = amphipod

                    next_amphipod = (type, 2, next_j, MOVING)

                    next_burrow.remove((ai, aj))
                    next_burrow.add((2, next_j))

                    next_amphipods[n] = next_amphipod

                    next_goals = list(goals) # copy, and make mutable
                    if amphipod[I] == 0: # last leaving a hallway
                        next_goals[amphipod[TYPE]] = True
                    actions.append((tuple(next_amphipods), next_burrow, tuple(next_goals), cost_to_go + (cost + 2 - amphipod[I]) * SETTINGS[amphipod[TYPE]][ENERGY], heuristic(next_amphipods)))

            # try to go home if goal/hallway is open
            if amphipod[STATE] == MOVING and goals[amphipod[TYPE]]:
                # print(f"{amphipod} wants to go to the hallway/goal")
                # print(amphipod[J], "->", SETTINGS[amphipod[TYPE]][HALLWAY])
                # print(free_spots(amphipod[J], SETTINGS[amphipod[TYPE]][HALLWAY], burrow))
                is_hallway_reachable, _ = free_spots(amphipod[J], SETTINGS[amphipod[TYPE]][HALLWAY], burrow)

                if is_hallway_reachable:
                    next_burrow = burrow.copy()
                    next_amphipods = list(amphipods)  # copy, and make mutable

                    type, ai, aj, state = amphipod

                    # cost to hallway entrance
                    cost = abs(aj - SETTINGS[amphipod[TYPE]][HALLWAY])

                    if (2, SETTINGS[amphipod[TYPE]][HALLWAY]) not in burrow:
                        first_amphipod = True
                        cost += 2
                    else:
                        first_amphipod = False
                        cost += 1

                    next_amphipod = (type, 2 if first_amphipod else 1, SETTINGS[amphipod[TYPE]][HALLWAY], READY)

                    next_burrow.remove((ai, aj))
                    next_burrow.add((2 if first_amphipod else 1, SETTINGS[amphipod[TYPE]][HALLWAY]))

                    next_amphipods[n] = next_amphipod

                    # no change in goals
                    actions.append((tuple(next_amphipods), next_burrow, goals, cost_to_go + cost * SETTINGS[amphipod[TYPE]][ENERGY], heuristic(next_amphipods)))

    return actions

# print(get_actions(amphipods, burrow, goals, 0))
#
# for amphipods, burrow, goals, cost in get_actions(amphipods, burrow, goals, 0):
#     print(get_actions(amphipods, burrow, goals, cost))

def a_star(amphipods, burrow, goals):
    # TODO: add explored, with occupied positions per type

    to_explore = [] # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (0, 0, amphipods, burrow, goals))

    while len(to_explore) > 0:
        estimated_cost, cost, amphipods, burrow, goals = heapq.heappop(to_explore)
        states = [x[STATE] == READY for x in amphipods]
        if sum(states) == len(amphipods):
            print("FOUND")
            return cost

        actions = get_actions(amphipods, burrow, goals, cost)
        for next_amphipods, next_burrow, next_goals, next_cost, estimated_cost in actions:

            heapq.heappush(to_explore, (next_cost + estimated_cost, next_cost, next_amphipods, next_burrow, next_goals))

    return "Not found"


print(a_star(amphipods, burrow, goals))

# test has min of 12521

# moeten a-b, twee per kamer
# in open.
# energy A = 1, B = 10, C = 100, D = 1000, least total energy.
# nooit stoppen voor een kamer
# alleen kamer in als je daar moet zijn, en er niemand is die daar niet hoort
# als je stopt in de gang, mag je pas weer lopen als je meteen naar een kamer loopt