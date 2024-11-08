import heapq
from functools import cache

from tools import stopwatch

file1 = open('q23c.txt', 'r')
file_lines = file1.readlines()

amphipods = []

HALLWAY_SIZE = 4

SETTINGS = {
    1: [2, 1],
    2: [4, 10],
    3: [6, 100],
    4: [8, 1000]
}

DESTINATION, ENERGY = 0, 1

INITIAL = 0
BURROW = INITIAL + 4 * HALLWAY_SIZE
GOAL = BURROW + 11 # don't need al, but will make calculations easier I hope

initial_state = [0] * (4 * HALLWAY_SIZE + 11 + 4 * HALLWAY_SIZE)

for i in range(HALLWAY_SIZE):
    situation = file_lines[2 + i].rstrip()
    for pos in range(len(situation)):
        if situation[pos] in ['A', 'B', 'C', 'D']:
            amphipods.append((ord(situation[pos]) - ord('A') + 1, i, pos - 1)) # 0 is bottom, pos is up

# create initial state from amphipods
for amphipod in amphipods:
    at, ai, aj = amphipod
    initial_state[(aj // 2 - 1) * HALLWAY_SIZE + (HALLWAY_SIZE - ai - 1)] = at


print(amphipods)

initial_state = tuple(initial_state)

# initial_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4)

goal_state = [0] * (HALLWAY_SIZE * 4 * 2 + 11)

for i in range(4):
    for h in range(HALLWAY_SIZE):
        goal_state[BURROW + 11 + HALLWAY_SIZE * i + h] = i + 1
goal_state = tuple(goal_state)

print(goal_state)


print(initial_state)

print("----------")


# move initial amphipods to end state if they are already in place

new_initial_state = list(initial_state)

# TODO: fix hallway size
for i in range(0, 4):
    for h in range(HALLWAY_SIZE):
        amphipod = initial_state[i * HALLWAY_SIZE + h]

        if amphipod == (i + 1): # correct amphipod => move
            new_initial_state[BURROW + 11 + (i * HALLWAY_SIZE + h)] = amphipod
            new_initial_state[i * HALLWAY_SIZE + h] = 0
        else:
            break # not correct, break to next hallway, because everyone above must leave to make room

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

    # from burrow to destination
    for i in range(11):
        amphipod_type = state[BURROW + i]
        if amphipod_type == 0:  # empty
            continue

        # everyone needs to have left initial state before going to the goal
        if sum(state[HALLWAY_SIZE * (amphipod_type - 1): HALLWAY_SIZE * (amphipod_type - 1) + HALLWAY_SIZE]) > 0:
            continue

        # path free? # TODO: faster to put after goal empty?
        from_pos = i + BURROW
        to_pos = (amphipod_type - 1) * 2 + 2 + BURROW
        # reverse if not in right order
        if from_pos > to_pos:
            from_pos, to_pos = to_pos, from_pos

        if sum(state[from_pos:to_pos + 1]) > amphipod_type:  # obstruction because there must be someone else in the way
            continue

        steps = to_pos - from_pos

        # put amphipod at first free position
        for h in range(HALLWAY_SIZE):
            if state[GOAL + HALLWAY_SIZE * (amphipod_type - 1) + h] == 0:
                new_state = list(state)  # copy and make mutable
                new_state[GOAL + HALLWAY_SIZE * (amphipod_type - 1) + h] = new_state[i + BURROW]
                new_state[i + BURROW] = 0
                states.append((tuple(new_state), (steps + HALLWAY_SIZE - h) * SETTINGS[amphipod_type][ENERGY]))

                break

    # if it is possible to go home, do not move other pieces
    if len(states) == 0:
        # from initial state to burrow
        for i in range(4):
            for h in range(HALLWAY_SIZE):
                amphipod = state[i * HALLWAY_SIZE + h]
                if amphipod == 0: # empty
                    continue
                steps = 0

                if sum(state[i * HALLWAY_SIZE + h: (i+1) * HALLWAY_SIZE]) > amphipod: # is someone in the way?
                    continue
                else:
                    steps += (HALLWAY_SIZE - h)
                for new_index, extra_steps in get_reachable_places(i * 2 + 2, state):
                    new_state = list(state) # copy and make mutable
                    new_state[new_index] = new_state[i * HALLWAY_SIZE + h]
                    new_state[i * HALLWAY_SIZE + h] = 0
                    # get_reachable returns one too many
                    states.append((tuple(new_state), (steps + extra_steps - 1) * SETTINGS[amphipod][ENERGY]))

    return states


# TODO: create memoised helper functions to calc heuristic

@cache
def heuristic_initial(partial_state):
    estimated_cost = 0
    # cost to get to burrow (and above destination)
    for i in range(4):
        for h in range(HALLWAY_SIZE):
            amphipod = partial_state[i * HALLWAY_SIZE + h]
            if amphipod == 0:
                continue
            estimated_cost += SETTINGS[amphipod][ENERGY] * (HALLWAY_SIZE - h)

            # burrow
            to_pos = (amphipod - 1) * 2 + 2
            estimated_cost += abs((i * 2 + 2) - to_pos) * SETTINGS[amphipod][ENERGY]

    return estimated_cost

@cache
def heuristic_burrow(partial_state):
    estimated_cost = 0

    # cost to get above destination (already in burrow)
    for i in range(11):
        amphipod = partial_state[i]
        if amphipod == 0:
            continue
        to_pos = (amphipod - 1) * 2 + 2
        estimated_cost += abs(i - to_pos) * SETTINGS[amphipod][ENERGY]

    return estimated_cost

@cache
def heuristic_end(partial_state):
    estimated_cost = 0

    # cost to get inside destination (everyine who is not home yet)
    for i in range(4):
        for h in range(HALLWAY_SIZE):
            amphipod = partial_state[i * HALLWAY_SIZE + h]
            if amphipod > 0:
                continue
            estimated_cost += SETTINGS[i + 1][ENERGY] * (HALLWAY_SIZE - h)

    return estimated_cost

def heuristic(state):
    estimated_cost = heuristic_initial(state[0:BURROW])

    estimated_cost += heuristic_burrow(state[BURROW: BURROW + 11])

    estimated_cost += heuristic_end(state[BURROW + 11:])


    return estimated_cost
def a_star(start, goal):
    explored = set()
    to_explore = [] # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (heuristic(start), 0, start))

    while len(to_explore) > 0:
        estimated_cost, cost_so_far, state = heapq.heappop(to_explore)

        # print(estimated_cost)

        if state in explored:
            continue
        explored.add(state)
        # print(state)
        if state == goal:
            print("FOUND")
            return cost_so_far

        actions = get_next_states(state)
        for next_state, next_cost in actions:
            # print("NEXT:", next_state)
            if next_state in explored: # don't explore again
                continue

            # print("A", next_state, next_cost)

            heapq.heappush(to_explore, (heuristic(next_state) + cost_so_far + next_cost, next_cost + cost_so_far, next_state))
            # explored.add(next_state)
    return "Not found"


stopwatch.start("astar")
print(">>", a_star(initial_state, goal_state))
stopwatch.stop("astar")
stopwatch.show()

# for state in get_next_states(initial_state):
#     print(state)


# 44169 too low