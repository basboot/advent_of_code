import hashlib
import math
from collections import Counter, deque

import numpy as np

import networkx as nx
from collections import defaultdict

# grid 4x4, start at 0,0 target 0,3, cannot go outside grid, can walk only if passcode permits
# grid changes during wals, so bfs is probably the best idea

passcode = "qtetzkpl"

def doors_unlocked(passcode):
    result = hashlib.md5(passcode.encode()).hexdigest()

    locks = [result[i] in {'b', 'c', 'd', 'e','f'} for i in range(4)]

    return locks # up, down, left, and right

def get_actions(position, unlocked):
    # print(passcode)
    # print(unlocked)
    actions = []
    i, j = position
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    moves = ("U", "D", "L", "R")
    for n in range(len(directions)):
        di, dj = directions[n]
        ni, nj = i + di, j + dj
        if 0 <= ni <= 3 and 0 <= nj <= 3 and unlocked[n]:
            actions.append(((ni, nj), moves[n]))

    return actions


def bfs(start, goal):
    queue = deque([(start, "")])
    # we cannot use a visited set :-(

    longest_path = -math.inf
    shortest_path = None

    while queue:
        current_pos, path = queue.popleft()

        if current_pos == goal:
            # update longest path
            longest_path = max(len(path), longest_path)
            # store shortest path
            if shortest_path is None:
                shortest_path = path

            continue

        for action in get_actions(current_pos, doors_unlocked(passcode + path)):
            new_pos, step = action
            new_path = path + step
            queue.append((new_pos, new_path))

    return shortest_path, longest_path

part1, part2 = bfs((0, 0), (3, 3))

print("Part 1", part1)
print("Part 2", part2)