# Using readlines()
from networkx import shortest_path

from tools.advent_tools import *

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

maze = []

for line in lines:
    maze.append(list(line.rstrip()))

print(maze)

RECURSE_DEPTH = 30

def get_maze(i, j):
    if i < 0 or j < 0 or i >= len(maze) or j >= len(maze[i]):
        return None
    else:
        return maze[i][j], i < 2 or j < 2 or i >= len(maze) - 2 or j >= len(maze[i]) - 2
def get_neighbours(i, j):
    neighbours = []
    for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        tile, outside = get_maze(i + di, j + dj)
        assert tile is not None, "Assumption . is never at the boundary is not correct"

        if tile == ".":
            neighbours.append((str((i + di, j + dj)), outside))
        else:
            if tile.isalpha(): # portal
                next_tile, outside = get_maze(i + 2*di, j + 2*dj)
                if (di, dj) in [(-1, 0), (0, -1)]:
                    neighbours.append((next_tile + tile, outside)) # up and left read reversed
                else:
                    neighbours.append((tile + next_tile, outside))

    return neighbours

import networkx as nx
G = nx.Graph()

for i in range(len(maze)):
    row = maze[i]
    for j in range(len(row)):
        if row[j] == ".":
            for neighbour, outside in get_neighbours(i, j):
                for level in range(RECURSE_DEPTH):
                    if neighbour[0].isalpha():
                        if neighbour in ['AA', 'ZZ']: # AA en ZZ only connected to outside:
                            if level == 0:
                                G.add_edge(str((i, j)) + f"level{level}", neighbour, weight=0.5)  # portals length 1 for stepping in and out
                        else:
                            if outside:
                                if level > 0: # other outsides only connected on deeper levels
                                    # print("out", neighbour)
                                    G.add_edge(str((i, j)) + f"level{level}", neighbour + f"level{level - 1}", weight=0.5)
                            else:
                                # print("in", neighbour)
                                G.add_edge(str((i, j)) + f"level{level}", neighbour + f"level{level}", weight=0.5)
                    else:
                        G.add_edge(str((i, j)) + f"level{level}", neighbour + f"level{level}", weight=1)


# for node in G.edges:
#     print(node)
#
# exit()
# # add nodes
# for tile in map:
#     if map[tile] != "#":
#         G.add_node((tile))
#
# # add edges
# for tile in map:
#     if map[tile] != "#":
#         for action in [NORTH, EAST, SOUTH, WEST]:
#             n, _ = next_pos(tile, action)
#             if n not in trees:
#                 G.add_edge(tile, n)
#                 G[tile][n]["weight"] = 1 # initial weight of edge


shortest = shortest_path(G, source="AA", target="ZZ", weight="weight", method='dijkstra')
print(shortest)

total = 0
for i in range(len(shortest) - 1):
    # print(G.edges[shortest[i], shortest[i + 1]])
    total += G.edges[shortest[i], shortest[i + 1]]["weight"]

print(total - 1) # -1, remove stepping in and out of the maze