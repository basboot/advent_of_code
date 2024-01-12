import math
import numpy as np

file1 = open('q5a.txt', 'r')
file_lines = file1.readlines()

lines = []
max_x = -math.inf
max_y = -math.inf

for file_line in file_lines:
    line = [tuple([int(x) for x in p.split(",")]) for p in file_line.rstrip().split(" -> ")]
    lines.append(line)

    max_x = max(max_x, line[0][0], line[1][0])
    max_y = max(max_y, line[0][1], line[1][1])


 # Note that coordinates are reversed, but this makes it easier to think in x and y
 # Also coordinates are 1 indexed instead of 0 (+1)
world = np.zeros((max_x + 1, max_y + 1), dtype=int)

print(world)

hor_lines = []
ver_lines = []

for line in lines:
    if line[0][0] == line[1][0]:
        # top to bottom
        if line[0][1] > line[1][1]:
            ver_lines.append([line[1], line[0]])
        else:
            ver_lines.append(line)
    if line[0][1] == line[1][1]:
        # always from left to right
        if line[0][0] > line[1][0]:
            hor_lines.append([line[1], line[0]])
        else:
            hor_lines.append(line)

    # ignore diagonals for part 1

print("ver", ver_lines)
print("hor", hor_lines)

all_lines = hor_lines + ver_lines
for from_point, to_point in all_lines:
    world[from_point[0]:to_point[0] + 1, from_point[1]: to_point[1] + 1] += 1

print(np.transpose(world))
print("Part 1", len(np.where(world > 1)[0]))


for line in lines:
    # hor and vert already done
    if line[0][0] == line[1][0]:
        continue
    if line[0][1] == line[1][1]:
        continue

    # add diagonals for part 2
    dx = line[0][0] - line[1][0]
    dy = line[0][1] - line[1][1]

    n_blocks = abs(dx) + 1
    step_x = dx // abs(dx)
    step_y = dy // abs(dy)

    x = line[1][0]
    y = line[1][1]

    print(line)
    for i in range(n_blocks):
        print(x, y)
        world[x, y] += 1
        x += step_x
        y += step_y

print(np.transpose(world))
print("Part 2", len(np.where(world > 1)[0]))