import sys

import networkx as nx
import numpy as np
from executing import cache
from fontTools.misc.cython import returns
from networkx.algorithms.shortest_paths.weighted import dijkstra_path, dijkstra_path_length, \
    single_source_dijkstra_path, single_source_dijkstra

depth = 6969
target = (9, 796)

ROCKY, WET, NARROW = 0, 1, 2

erosion_level_map = np.zeros((target[0] + 1, target[1] + 1), dtype=object)

@cache
def erosion_level(position: (int, int)):
    x, y = position
    assert x >= 0 and y >= 0, "Negative position not allowed"
    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    if position == (0, 0) or position == target:
        return 0

    # If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    if y == 0:
        return (x * 16807 + depth) % 20183

    # If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    if x == 0:
        return (y * 48271 + depth) % 20183

    # Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.
    g1 = erosion_level((x - 1, y))
    g2 = erosion_level((x, y - 1))
    return (g1 * g2 + depth) % 20183


def region_type(position):
    return erosion_level(position) % 3

total = 0
for y in range(target[1] + 1):
    for x in range(target[0] + 1):
        position = (x, y)
        rt = region_type(position)
        total += rt

print("Part 1", total)

G = nx.Graph()

NEITHER, TORCH, CLIMBING = 0, 1, 2
equipment = [NEITHER, TORCH, CLIMBING]
legal_equipment = {
    ROCKY: {CLIMBING, TORCH},
    WET: {CLIMBING, NEITHER},
    NARROW: {TORCH, NEITHER}
}

for y in range(target[1] + 1 + 50): # extra room outside the map
    for x in range(target[0] + 1 + 50):
        from_type = region_type((x, y))
        # to other gear
        for from_gear in equipment:
            for to_gear in equipment:
                if from_gear != to_gear and from_gear in legal_equipment[from_type] and to_gear in legal_equipment[from_type]:
                    if (x == 4) and (y == 1):
                        print("**", from_gear, to_gear)
                    G.add_edge((x, y, from_gear), (x, y, to_gear), weight=7)  # 7 minutes

        # to other region
        for dy, dx in [-1, 0], [1, 0], [0, -1], [0, 1]:
            next_x = x + dx
            next_y = y + dy

            # stay inside boundaries
            if 0 <= next_x and 0 <= next_y:

                to_type = region_type((next_x, next_y))

                for gear in equipment:
                    # gear must be legal in both environments
                    if gear in legal_equipment[from_type] and gear in legal_equipment[to_type]:
                        G.add_edge((x, y, gear), (next_x, next_y, gear), weight=1) # 1 minute



print(G)

path = single_source_dijkstra(G, (0, 0, TORCH), (target[0], target[1], TORCH), weight='weight')

print("solution", path)

# for i in range(len(path[1]) - 1):
#     print(path[1][i], path[1][i + 1], G.edges[(path[1][i], path[1][i + 1])])
#
# 1153 too high
# 1109 too high
# need to go 'outside'
# 1085 too low, strange... error in AoC? -> 1087 strange?


