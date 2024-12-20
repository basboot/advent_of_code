from collections import deque

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

walls = set()

start = goal = steps_no_cheating = None # to suppress warnings

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

def next_options(position, cheats, cheat_start, cheat_end):
    i, j = position
    options = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        # we need to check boundaries to avoid escaping through wall # TODO
        if not (0 <= ni < m and 0 <= nj < n):
            continue
        if (ni, nj) not in walls:
            # 1 means you stepped out of a wall, so lose the second cheat.
            # check is last move was cheating to detect cheat end
            last_move_cheating = cheat_end is None and cheat_start is not None
            options.append(((ni, nj), cheats, cheat_start, (ni, nj) if last_move_cheating else cheat_end, last_move_cheating))
        else:
            if cheats > 0:
                # move in wall so remove one cheat, cheat starts if cheats was 2
                # set cheat end to (-1, -1) to detect last move was cheating
                options.append(((ni, nj), cheats - 1, (i, j), cheat_end, False))
    return options

def bfs(start, goal, cheating):
    cheats = 1 if cheating else 0
    # only interested in cheat points
    unique_cheats = set()

    to_explore = deque([(0, start, cheats, {start}, None, None)])

    while len(to_explore) > 0:
        steps, position, cheats, visited, cheat_start, cheat_end = to_explore.popleft()

        if position == goal:
            yield steps, cheat_start, cheat_end

        for next_position, next_cheats, next_cheat_start, next_cheat_end, cheat_found in next_options(position, cheats, cheat_start, cheat_end):
            if next_position in visited:
                continue # dont visit twice

            if cheat_found:
                if (next_cheat_start, next_cheat_end) in unique_cheats:
                    continue # no need to look further, we already found this
                else:
                    unique_cheats.add((next_cheat_start, next_cheat_end))

            # bfs, so invalidate early
            to_explore.append((steps + 1, next_position, next_cheats, visited.union({next_position}), next_cheat_start, next_cheat_end))

    print(unique_cheats)
    print(len(unique_cheats))
    return None

for steps in bfs(start, goal, 0):
    steps_no_cheating, _, _ = steps
    # we only need the first without cheating as a reference
    break

print("No cheats", steps_no_cheating)

min_gain = 4

total = 0
for steps, cheat_start, cheat_end in bfs(start, goal, 2):
    # ignore illegal cheats
    if steps > steps_no_cheating - min_gain:
        break
    print("steps", steps, cheat_start, cheat_end)
    total += 1



print(total)
