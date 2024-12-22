from collections import deque

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

walls = set()

start = goal = None # to suppress warnings

for i, line in enumerate(lines):
    for j, char in enumerate(list(line.rstrip())):
        match char:
            case "#":
                walls.add((i, j))
            case "S":
                start = (i, j)
            case "E":
                goal = (i, j)

m, n = len(lines), len(lines[0].rstrip())

def next_options(position, in_wall=False):
    i, j = position
    options = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        # we need to check boundaries to avoid escaping through wall
        if not (0 <= ni < m and 0 <= nj < n):
            continue

        if in_wall:
            if (ni, nj) in walls:
                options.append((ni, nj))

        if (ni, nj) not in walls:
                options.append((ni, nj))

    return options

def next_cheat_options(position, cheat_seconds):
    options = []
    visited = {position}
    to_explore = deque([(0, position)])

    while len(to_explore) > 0:
        steps, position = to_explore.popleft()

        # time up
        if steps > cheat_seconds:
            break

        # found way out of wall
        if position not in walls and steps > 0:
            if steps > 1: # skip normal walk
                options.append((steps, position))

        for next_position in next_options(position, True):
            if next_position in visited:
                continue  # dont visit twice

            # bfs, so invalidate early
            visited.add(next_position)
            to_explore.append((steps + 1, next_position))

    return options

def create_lookup_table(goal):
    distances = {}
    visited = {goal}
    to_explore = deque([(0, goal)])

    while len(to_explore) > 0:
        steps, position = to_explore.popleft()

        distances[position] = steps

        for next_position in next_options(position):
            if next_position in visited:
                continue # dont visit twice

            # bfs, so invalidate early
            visited.add(next_position)
            to_explore.append((steps + 1, next_position))

    return distances

def find_cheats(start, goal, distances, cheat_seconds):
    cheats = {}
    visited = {start}
    to_explore = deque([(0, start)])

    while len(to_explore) > 0:
        steps, position = to_explore.popleft()

        if position == goal:
            # found goal without cheating, no use to look further
            break

        for next_position in next_options(position):
            if next_position in visited:
                continue # dont visit twice

            # bfs, so invalidate early
            visited.add(next_position)
            to_explore.append((steps + 1, next_position))

        # try to cheat
        for extra_steps, next_position in next_cheat_options(position, cheat_seconds):
            if (position, next_position) in cheats:
                # I don't think this can happen with the new search
                assert cheats[(position, next_position)] > steps + extra_steps + distances[next_position], "we invalidate too early"
                continue # dont visit twice

            cheats[(position, next_position)] = steps + extra_steps + distances[next_position]

    return cheats



distances = create_lookup_table(goal)
print("No cheating", distances[start])

cheats = find_cheats(start, goal, distances, 20)

total = 0
for position, distance in cheats.items():
    if distance <= distances[start] - 100:
        # print(position, distance)
        total += 1
print(total)

# 221404 too low
#
# for steps, option in next_cheat_options((5, 0), 10):
#     print(steps, option)


# 221615 (sort)

# volgorde?

# 1098668 too high