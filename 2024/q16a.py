import heapq

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

start = None
goal = None
maze = set()

for i, line in enumerate(lines):
    for j, cell in enumerate(list(line.rstrip())):
        position = i + j*1j
        match cell:
            case "S":
                start = position
            case "E":
                goal = position
            case "#":
                maze.add(position)


def get_next_options(position, orientation):
    options = []
    # check for walls
    if position + orientation not in maze:
        options.append((1, position + orientation, orientation))
    # turn always possible, but only allow if there is something to turn to
    paths = sum([1 if (position + look) not in maze else 0 for look in [1, -1, 1j, -1j]])
    if paths > 1:
        options += [(1000, position, orientation * turn) for turn in [-1j, 1j]]
    return options



def dijkstra(start, goal, orientation, start_cost):
    visited = set()
    to_explore = []
    heapq.heappush(to_explore, (start_cost, start.real, start.imag, orientation.real, orientation.imag, {start})) # cost to go, position real, position imag, orientation

    best_places = set()
    best_score = None

    while len(to_explore) > 0:
        cost, pos_real, pos_imag, or_real, or_imag, path = heapq.heappop(to_explore)
        position = pos_real + pos_imag * 1j
        orientation = or_real + or_imag * 1j

        if position == goal:
            if best_score is None:
                best_score = cost
                best_places = path
            else:
                if cost > best_score:
                    return best_score, len(best_places)
                else:
                    print("found other best path")
                    best_places = best_places.union(path)

        visited.add((position, orientation)) # TODO: can this be done earlier? I'm not sure for this example

        for cost_next_step, next_position, next_orientation in get_next_options(position, orientation):
            if (next_position, next_orientation) not in visited:
                heapq.heappush(to_explore, (cost + cost_next_step, next_position.real, next_position.imag, next_orientation. real, next_orientation.imag, path.union({next_position})))

    return best_score, len(best_places)



        # start facing East (1j), but turn north to help (costs 1000)
print(dijkstra(start, goal, -1, 1000))

total = 0

print(f"Part 1, {total}")
