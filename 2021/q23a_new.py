import heapq
from functools import cache

file1 = open('q23a.txt', 'r')
file_lines = file1.readlines()

amphipods = []

HALLWAY_SIZE = 2

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

for i in range(2):
    situation = file_lines[2 + i].rstrip()
    for pos in range(len(situation)):
        if situation[pos] in ['A', 'B', 'C', 'D']:
            amphipods.append((ord(situation[pos]) - ord('A') + 1, 1 - i, pos - 1)) # 0 is bottom, pos is up
            initial_state[(pos - 3) + (1 - i)] = ord(situation[pos]) - ord('A') + 1

print(amphipods)

initial_state = tuple(initial_state)

goal_state = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4)

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

    # from initial state to burrow
    for i in range(4 * HALLWAY_SIZE):
        amphipod_type = state[i]
        if amphipod_type == 0: # empty
            continue
        steps = 0
        if i % HALLWAY_SIZE == 0: # has to travel extra step(s) (and must have free space above)
            if state[i + 1] > 0: # TODO: check all above
                continue
            else:
                steps += 1 # TODO: add full hallway
        for new_index, extra_steps in get_reachable_places((i // HALLWAY_SIZE) * HALLWAY_SIZE + 2, state):
            new_state = list(state) # copy and make mutable
            new_state[new_index] = new_state[i]
            new_state[i] = 0
            states.append((tuple(new_state), (steps + extra_steps) * SETTINGS[amphipod_type][ENERGY]))

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

        if sum(state[from_pos:to_pos + 1]) > amphipod_type: # obstruction because there must be someone else in the way
            continue

        steps = to_pos - from_pos

        # put amphipod at first free position
        for h in range(HALLWAY_SIZE):
            if state[GOAL + HALLWAY_SIZE * (amphipod_type - 1) + h] == 0:
                new_state = list(state)  # copy and make mutable
                new_state[GOAL + HALLWAY_SIZE * (amphipod_type - 1) + h] = new_state[i + BURROW]
                new_state[i + BURROW] = 0
                states.append((tuple(new_state), (steps + HALLWAY_SIZE - h) * SETTINGS[amphipod_type][ENERGY]))

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


# print(">>", a_star(initial_state, goal_state))

for state in get_next_states(initial_state):
    print(state)


