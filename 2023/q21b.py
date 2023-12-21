# Using readlines()
from tools.advent_tools import *
import numpy as np

file1 = open('q21a.txt', 'r')
lines = file1.readlines()

from tabulate import tabulate

height = len(lines)
width = len(lines[0].rstrip())
rocks = set()
for i in range(height):
    for j in range(width):
        if lines[i].rstrip()[j] == "S":
            start = (i, j)
        if lines[i].rstrip()[j] == "#":
            rocks.add((i, j))


reachable = {}

# map repeats , so i % height is also on the map
def get_next_positions(pos):
    i, j = pos
    next_positions = []
    for ni, nj in [(i + di, j + dj) for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
        if (ni % height, nj % width) not in rocks:
            next_positions.append((ni, nj))
    return next_positions

N_MAPS_DATA = 4 # number of maps to walk (+ half the first)
MAX_STEPS = width // 2 + width * N_MAPS_DATA

maps_reached = set()
maps_sat = {}

next_positions = [start]
reachable[start] = 0 # modulus 2

# explore maps (bfs) and store when each position is first reached (and can be reached modulo 2 again)
for step in range(MAX_STEPS):
    positions = next_positions
    next_positions = []
    while len(positions) > 0:
        pos = positions.pop() # order does not matter

        for pos in get_next_positions(pos):
            if pos in reachable:
                continue # don't visit again
            else:
                next_positions.append(pos)
                i, j = pos
                map_i, map_j = math.floor(i / height), math.floor(j / width)
                if (map_i, map_j) not in maps_reached:
                    # print(f"reached map ({map_i}, {map_j}) at step {step + 1}")
                    maps_reached.add((map_i, map_j))
                    maps_sat[(map_i, map_j)] = { "start": step + 1}

                reachable[pos] = step + 1 # admin when reachable, and don't visit again

print(f"# maps {len(maps_reached)}")

# number of tiles reachable on one of the (repeating) maps
def reachable_on_map(map_i, map_j, odd=True):
    total = 0
    for i in range(height):
        for j in range(width):
            if (i + map_i * height, j + map_j * width) in reachable:
                if reachable[(i + map_i * height, j + map_j * width)] % 2 == (1 if odd else 0):
                    total += 1
    return total

# map zero, to find saturation
print("map 0 odd", reachable_on_map(0, 0))
print("map 0 even", reachable_on_map(0, 0, odd=False))

# show # reachable tiles per map
table = []
data = []
for i in range(-N_MAPS_DATA, N_MAPS_DATA + 1, 1):
    row = []
    data_row = []
    for j in range(-N_MAPS_DATA, N_MAPS_DATA + 1, 1):
        n = reachable_on_map(i, j)
        if n > 0:
            row.append(n)
            data_row.append(n)
        else:
            row.append(" ") # for pretty printing ;-)
    table.append(row)
    data.append(data_row)

print(tabulate(table))

# construct reachability based on data from visited maps
# map is 133x333
N_MAPS_CONSTRUCT = 202300 # 26501365 steps => 65 steps to get of first map, and (26501365 - 65) = 202300 * 133 for next

# def interpolate(data, desired_len):
#     assert desired_len % 2 == len(data) % 2, "can only add even numbers of data"
#     while len(data) < desired_len:
#         data = data[:(len(data) // 2)] + [data[len(data) // 2], data[len(data) // 2 + 1]] + data[(len(data) // 2):]
#     return data
#
# constructed_reachability = 0


# for row in range(N_MAPS_CONSTRUCT * 2 + 1):
#     if row % 1000 == 0:
#         print(row)
#     if row == N_MAPS_CONSTRUCT:
#         selected_data = interpolate(data[N_MAPS_DATA], 1 + N_MAPS_CONSTRUCT * 2) # use middle row from data
#     else:
#         if row > N_MAPS_CONSTRUCT:
#             r_data = N_MAPS_CONSTRUCT * 2 - row
#         else:
#             r_data = row
#         n_data = min(N_MAPS_DATA - 1, r_data) # middle row cannot be used
#         if row > N_MAPS_CONSTRUCT:
#             n_data = len(data) - 1 - n_data # from other side
#
#         selected_data = data[n_data]
#         selected_data = interpolate(selected_data, 3 + r_data * 2)
#     # print(selected_data)
#     constructed_reachability += sum(selected_data)
#
# print(f"Simulated {width // 2 + width * N_MAPS_CONSTRUCT} steps")
# print(f"Reached {constructed_reachability} (simulated construction)")


# calculate reachability for N_MAPS_CONSTRUCT based on experienced data of N_MAPS_DATA

# use first and last rows as is
reachable = sum(data[0] + data[1] + data[-1] + data[-2])
# add middle row, because it is different (is too small needs to be corrected later)
reachable += sum(data[N_MAPS_DATA])

# add two rows around (real rows), and use copies to get enough rows
# assumption maps = even
assert N_MAPS_CONSTRUCT % 2 == 0, "Cannot be used for odd constructions"

# real rows
reachable += (sum(data[N_MAPS_DATA - 1] + data[N_MAPS_DATA - 2] + data[N_MAPS_DATA + 1] + data[N_MAPS_DATA + 2]))
# simulated
reachable += (sum(data[N_MAPS_DATA - 1] + data[N_MAPS_DATA - 2] + data[N_MAPS_DATA + 1] + data[N_MAPS_DATA + 2])) * ((N_MAPS_CONSTRUCT - 4) / 2)

# and add the missing inner part for the simulated rows

# tiles are added in paires, because size is odd, we need to add an odd and an even reachablity each time
odd_even_reach = data[N_MAPS_DATA][len(data[N_MAPS_DATA]) // 2] + data[N_MAPS_DATA][len(data[N_MAPS_DATA]) // 2 + 1]
# (1 + 2 + 3 + ...) * 2 increase per row, and add one extra on every second row because it is smaller than the first
n = (N_MAPS_CONSTRUCT - 4)
reachable += (((n * (n + 1))) / 2 + n) * odd_even_reach * 2

print("Number of reachable tiles:", reachable)
print(f"Calculated {width // 2 + width * N_MAPS_CONSTRUCT} steps")



# print("Mapsize", width, height)
# print("Calc", 26501365 - 65, (26501365 - 65) / 131, (26501365 - 65) % 131)
