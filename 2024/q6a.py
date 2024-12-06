import numpy as np

file1 = open('q6a.txt', 'r')
lines = file1.readlines()

direction = -1j
start = 0j
obstacles = set()

for i, line in enumerate(lines):
    for j, value in enumerate(list(line.rstrip())):
        match value:
            case '^':
                start = j + i * 1j
            case '#':
                obstacles.add(j + i * 1j)

grid_size = len(lines) # grid is a rectangle

visited = set()
path = set()

next_guard = start

while -1 < next_guard.real < grid_size and -1 < next_guard.imag < grid_size:
    # take step
    guard = next_guard
    visited.add(guard)

    # move or turn?
    next_guard = guard + direction
    if next_guard in obstacles:
        next_guard = guard # reset pos
        direction *= 1j # turn

print(f"Part 1, {len(visited)}")

def creates_loop(obstacle, start):
    new_path = set()
    direction = -1j

    next_guard = start

    while -1 < next_guard.real < grid_size and -1 < next_guard.imag < grid_size:
        # take step
        guard = next_guard

        # guard has been in this pos + dir before => loop
        if (guard, direction) in new_path:
            return True

        new_path.add((guard, direction))

        # move or turn?
        next_guard = guard + direction
        if next_guard in obstacles or next_guard == obstacle:
            next_guard = guard  # reset pos
            direction *= 1j  # turn

    return False # guard 'escapes', no loop

total = 0
# put obstacle on all visited places after start
for position in visited:
    if position == start:
        continue
    if creates_loop(position, start):
        total += 1

print("Part 2", total)

