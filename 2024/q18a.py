from collections import deque

file1 = open('q18a.txt', 'r')
lines = file1.readlines()

# 2913

max_t = 1024
memory_size = 70

blocking_bytes = set()

show_not_falling = True
for i, line in enumerate(lines):
    x, y = map(int, line.rstrip().split(","))

    if i < max_t:
        blocking_bytes.add((x, y))
    else:
        if show_not_falling:
            print(x, y)
            show_not_falling = False

# add borders
for n in range(memory_size + 1):
    blocking_bytes.add((n, -1))
    blocking_bytes.add((n, memory_size + 1))
    blocking_bytes.add((-1, n))
    blocking_bytes.add((memory_size + 1, n))

start = (0, 0)
goal = (memory_size, memory_size)

def next_options(position):
    x, y = position
    options = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in blocking_bytes:
            options.append((nx, ny))
    return options

def bfs(start, goal):
    visited = {start}
    to_explore = deque([(0, start)])

    while len(to_explore) > 0:
        steps, position = to_explore.popleft()

        if position == goal:
            return steps

        for next_position in next_options(position):
            if next_position in visited:
                continue # dont visit twice

            # bfs, so invalidate early possible
            visited.add(next_position)

            to_explore.append((steps + 1, next_position))

    return None

print(bfs(start, goal))
