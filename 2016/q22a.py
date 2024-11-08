import heapq
import re
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

file1 = open('q22a.txt', 'r')

lines = file1.readlines()

not_empty_nodes_usage = {}
available_data_nodes = defaultdict(set)

cells = {}

max_x = 0
max_y = 0

for i in range(2, len(lines)):
    line = lines[i]
    # x, y, Size, Used, Avail, Use
    x, y, total_size, used, avail, usage_pct = [int(x) for x in re.sub(r'\s+', ' ', line.rstrip()).replace("/dev/grid/node-x", "").replace("-y", " ").replace("T", "").replace("%", "").split(" ")]

    cells[(x, y)] = (total_size, used)
    max_x = max(x, max_x)
    max_y = max(y, max_y)

    id = (x, y)

    if used > 0:
        not_empty_nodes_usage[id] = used
    else:
        print("empty", x, y)
        print(cells[(x, y)])

    available_data_nodes[avail].add(id)

# create initial usage and capacity matrices
usage = np.zeros((max_y + 1, max_x + 1))
capacity = np.zeros((max_y + 1, max_x + 1))

print(max_x, max_y)
print(cells[(26, 22)])
for x in range(max_x + 1):
    for y in range(max_y + 1):
        if x == 26 and y == 22:
            print("***")
        cell_capacity, cell_usage = cells[(x, y)]
        usage[y, x] = cell_usage
        if usage[y, x] == 0:
            print("FOUND")
        capacity[y, x] = cell_capacity
        # print(f"{cell_usage} / {cell_capacity}", end=" | ")

    # print()

part1 = True

print(usage[22, 26])

if part1:
    sorted_availability = sorted(list(available_data_nodes.keys()), reverse=True)
    print(sorted_availability)

    pairs = 0
    for node in not_empty_nodes_usage:
        for availability in sorted_availability:
            if availability < not_empty_nodes_usage[node]:
                break
            pairs = pairs + len(available_data_nodes[availability]) # number of nodes on which usage will fit
            if node in available_data_nodes[availability]:
                pairs -= 1 # remove self if needed

    print("Part 1", pairs)



print(usage.shape)

m, n = usage.shape

fig, ax = plt.subplots()

# grid
for i in range(m + 1):
    ax.plot([0, n], [i, i], color='black', linewidth=0.2)  # Horizontal lines
for j in range(n + 1):
    ax.plot([j, j], [0, m], color='black', linewidth=0.2)  # Vertical lines

ax.set_xlim(0, n)
ax.set_ylim(0, m)
ax.invert_yaxis()  # Invert the y-axis to have (0,0) at the top-left corner

ax.axis('off')

def can_move(i, j):
    for di, dj in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n: # inside
            if usage[i, j] <= capacity[ni, nj] - usage[ni, nj]:
                return True
    return False

# Add usage
for i in range(m):
    for j in range(n):
        ax.text(j + 0.2, i + 0.2, str(int(usage[i, j])), color=('red' if usage[i, j] == 0 else 'black') if usage[i,j] < 100 else 'red',
                ha='center', va='center', fontsize=2)
        ax.text(j + 0.5, i + 0.5, str(int(capacity[i, j]) - int(usage[i, j])), color='black',
                ha='center', va='center', fontsize=4)
        ax.text(j + 0.8, i + 0.8, str(int(capacity[i, j])), color='black',
                ha='center', va='center', fontsize=2)

plt.savefig("q22.pdf", format='pdf', bbox_inches='tight')

plt.show()

# code below takes too long on the real problem. new approach => draw the grid to see if we can solve by hand,
# or find some properties we can exploid in the a star searcg

exit()
# NOTE: i, j = y, x
current_position = 0, max_x
goal_position = 0, 0

M, N = usage.shape

def get_next_states(current_usage, current_position):
    for i in range(M):
        for j in range(N):
            # try to move current data to all 4 sides, and yield state
            needed = current_usage[i, j]
            if needed == 0: # no need to move zero bytes
                continue
            for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                to_i, to_j = i + di, j + dj
                if 0 <= to_i < M and 0 <= to_j < N: # only move inside
                    space = capacity[to_i, to_j] - current_usage[to_i, to_j]
                    if space >= needed: # only move if it fits
                        new_usage = current_usage.copy()
                        # add needed to new node
                        new_usage[to_i, to_j] += needed
                        # empty old node
                        new_usage[i, j] = 0
                        yield new_usage, (current_position if current_position != (i, j) else (to_i, to_j))

# print("START")
# print(usage, current_position)
# for u, p in get_next_states(usage, current_position):
#     print(u, p)


def heuristic(position):
    i, j = position
    return abs(i) + abs(j)

def a_star(start, goal, usage):
    open_list = []
    id = (tuple(map(tuple, usage)), start)
    heapq.heappush(open_list, (heuristic(start), 0, id))
    closed = set()

    while open_list:
        estimated_cost, real_cost, id = heapq.heappop(open_list)

        # print(id)

        current_usage, current_position = id
        current_usage = np.array(current_usage)

        if current_position == goal:
            print("FOUND", real_cost)
            return

        for new_usage, new_position in get_next_states(current_usage, current_position):
            id = (tuple(map(tuple, new_usage)), new_position)
            if id in closed:
                continue

            closed.add(id)
            heapq.heappush(open_list, (heuristic(new_position) + real_cost, real_cost + 1, id))

a_star(current_position, goal_position, usage)




