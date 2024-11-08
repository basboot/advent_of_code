favorite_number = 1352

from collections import deque

def bfs(start, goal):
    queue = deque([[start]])
    visited = set()
    visited.add(start)

    while queue:
        path = queue.popleft()
        current_pos = path[-1]

        if current_pos == goal:
            return path

        for action in get_actions(current_pos):
            if action not in visited:
                visited.add(action)
                new_path = path.copy()
                new_path.append(action)
                queue.append(new_path)
    return None

def bfs2(start, steps):
    queue = deque([[start]])
    visited = set()
    visited.add(start)

    while queue:
        path = queue.popleft()
        if len(path) > 50:
            continue
        current_pos = path[-1]

        if current_pos == goal:
            return path

        for action in get_actions(current_pos):
            if action not in visited:
                visited.add(action)
                new_path = path.copy()
                new_path.append(action)
                queue.append(new_path)
    return visited

def is_open_space(x, y):
    if x < 0 or y < 0:
        return False # cannot go outside
    n = x*x + 3*x + 2*x*y + y + y*y
    n += favorite_number
    return bin(n).count('1') % 2 == 0

def get_actions(pos):
    x, y = pos
    actions = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if is_open_space(x + dx, y + dy):
            actions.append((x + dx, y + dy))

    return actions

start = (1, 1)
goal = (31,39)

print("Part 1", len(bfs(start, goal)) - 1)

print("Part 2", len(bfs2(start, 50)))

# 715 too high
# 141 too high
