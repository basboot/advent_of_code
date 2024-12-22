from collections import deque

import numpy as np
from scipy.spatial.distance import cityblock

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

def next_options(position):
    i, j = position
    options = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        # we need to check boundaries to avoid escaping through wall
        if not (0 <= ni < m and 0 <= nj < n):
            continue

        if (ni, nj) not in walls:
                options.append((ni, nj))

    return options

def create_lookup_table(goal, m, n):
    distances = np.ones((m, n)) * np.inf
    visited = {goal}
    to_explore = deque([(0, goal)])

    while len(to_explore) > 0:
        steps, position = to_explore.popleft()

        distances[position[0], position[1]] = steps

        for next_position in next_options(position):
            if next_position in visited:
                continue # dont visit twice

            # bfs, so invalidate early
            visited.add(next_position)
            to_explore.append((steps + 1, next_position))

    return distances

distances_goal = create_lookup_table(goal, m, n)
print("No cheating", distances_goal[start[0], start[1]])

distances_start = create_lookup_table(start, m, n)

gain = 100
max_distance = distances_goal[start[0], start[1]] - gain

#Chat GPT hulpje
# Create grid of coordinates
x_indices, y_indices = np.meshgrid(np.arange(m), np.arange(n), indexing='ij')

# Calculate Manhattan distances
distances_goal_optimal = np.abs(x_indices - goal[0]) + np.abs(y_indices - goal[1])

indices = np.argwhere(distances_start + distances_goal_optimal < max_distance)
for idx in indices:
    print(f"Index: {tuple(idx)}, Value: {arr[tuple(idx)]}")

# TODO:

cheat = 20
total = 0
for i in range(m):
    for j in range(n):
        # no use to explore if most optimal would not be enough
        if distances_start[i, j] < max_distance + cityblock((i, j), goal):
            for di in range(-cheat, cheat + 1):
                for dj in range(-cheat + abs(di), cheat - abs(di) + 1):
                    ni, nj = i + di, j + dj
                    if not (0 <= ni < m and 0 <= nj < n):
                        continue # must be in bounds
                    if distances_start[i, j] + distances_goal[ni, nj] + abs(di) + abs(dj) <= max_distance:
                        total += 1

print(total)

# 979012









