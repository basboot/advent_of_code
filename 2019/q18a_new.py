import math
from functools import cache
from itertools import permutations

import numpy as np
import heapq

from networkx import shortest_path, shortest_path_length

file1 = open('q18a.txt', 'r')
lines = file1.readlines()


keys = {} # a: (i, j, 0)
doors = {} # A: (i, j, 0), (i, j, 1), ...
start = None


maze = []

for i in range(len(lines)):
    maze.append(list(lines[i].rstrip()))

print(maze)

import networkx as nx
G = nx.Graph()

def create_edges(i, j, maze, G, door=False):
    n = 0
    for di, dj in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        if maze[i + di][j + dj] == ".":
            G.add_edge((i, j, n), (i + di, j + dj, 0), weight=1)
            if door:
                n += 1
    return n

    # we asume there are no isolated dots


for i in range(len(maze)):
    for j in range(len(maze[0])):
        tile = maze[i][j]
        if tile == "#":
            continue # ignore walls

        # add edges from this tile to surrounding tiles
        number_of_nodes = create_edges(i, j, maze, G, tile.isupper())

        G.nodes[(i, j, 0)]["value"] = tile

        # if it is not a normal tile (.) store it
        if tile == "@":
            start = (i, j, 0)
            G.nodes[(i, j, 0)]["type"] = "start"
        if tile.islower():
            keys[tile] = (i, j, 0)
            G.nodes[(i, j, 0)]["type"] = "key"
        if tile.isupper():
            doors[tile] = []
            for n in range(number_of_nodes):
                doors[tile].append((i, j, n))
                G.nodes[(i, j, n)]["value"] = tile
                G.nodes[(i, j, n)]["type"] = "door"


# remove normal nodes (.) that have only 2 edges from graph
def shrink_graph():
    for n in G.nodes:
        if len(list(G.neighbors(n))) == 2 and G.nodes[n]["value"] == ".":
            n1, n2 = list(G.neighbors(n))
            # print("Can be removed: ", n)
            combined_weight = G.edges[(n, n1)]["weight"] + G.edges[(n, n2)]["weight"]
            G.remove_node(n)
            G.add_edge(n1, n2, weight=combined_weight)
            return True
    return False

# remove
while shrink_graph():
    pass

# for n in G.nodes:
#     print("NODE", n)
#     if "type" in G.nodes[n]:
#         print(">", G.nodes[n]["type"], G.nodes[n]["value"])
#     print("EDGES")
#     for neighbour in G.neighbors(n):
#         print("E:", G.edges[(n, neighbour)])

# print(G)
#
# print(keys)
# print(doors)

# open door by connecting its nodes with weight zero
def open_door(G, door):
    if door not in doors:
        return G
    nodes_to_connect = doors[door]
    for i in range(len(nodes_to_connect) - 1):
        G.add_edge(nodes_to_connect[i], nodes_to_connect[i+1], weight=0)
    return G

def reachable_keys(pos, keys_to_find):
    actions = []
    for key in keys_to_find:
        try:
            steps = shortest_path_length(G, source=pos, target=keys[key], weight="weight", method='dijkstra')
            # print(key, steps)
            actions.append((key, steps))
        except:
            # ignore unreachable keys
            pass
    return actions


# open_door(G, "A")

# reachable_keys(start, ["a", "b"])
# import matplotlib.pyplot as plt
# nx.draw(G)
# plt.show()


# state is current position, and keys to find

# # dijkstra not working with doors
# def dijkstra():
#     explored = set()
#     to_explore = []  # heapq (cost_so_far, pos, keys to find, graph)
#
#     # push start with no cost to heap
#     heapq.heappush(to_explore, (0, start, set(keys.keys()), G, [(start, 0, "")]))
#
#     while len(to_explore) > 0:
#         cost, pos, keys_to_find, G, path = heapq.heappop(to_explore)
#         if len(keys_to_find) == 0: # all keys found
#             print("FOUND", cost)
#             print(path)
#             exit()
#
#         actions = reachable_keys(pos, keys_to_find)
#         for key, steps in actions:
#             next_keys_to_find = keys_to_find.copy()
#             next_keys_to_find.remove(key)
#             next_pos = keys[key]
#
#             if (next_pos, tuple(next_keys_to_find)) in explored:  # don't explore again
#                 continue
#
#             next_cost = cost + steps
#             next_G = open_door(G.copy(), key.upper())
#
#             next_path = path.copy()
#             next_path.append((next_pos, steps, key))
#
#             heapq.heappush(to_explore, (next_cost, next_pos, next_keys_to_find, next_G, next_path))
#             explored.add((next_pos, tuple(next_keys_to_find)))
#
#     print("NOT FOUND")

# min_steps = math.inf

best_steps = {}

graphs = {
    tuple(set(keys.keys())): G
}

@cache
# dfs to find all keys
def find_keys(start, keys_to_find):
    G = graphs[keys_to_find]
    keys_to_find = set(keys_to_find)

    # TODO: remove steps, return remaining steps

    global min_steps
    if len(keys_to_find) == 0:
        # print(f"Found all keys in {steps} steps")
        # min_steps = min(min_steps, steps)
        # print(min_steps)
        print("asdf")
        return 0

    best = math.inf

    for key in keys_to_find:
        next_steps = None
        try:
            next_steps = shortest_path_length(G, source=start, target=keys[key], weight="weight", method='dijkstra')
        except:
            # ignore unreachable keys
            pass

        if next_steps is not None:



            next_keys_to_find = keys_to_find.copy()
            next_keys_to_find.remove(key)

            keys_id = tuple(next_keys_to_find)

            next_G = graphs[keys_id] if keys_id in graphs else open_door(G.copy(), key.upper())
            graphs[keys_id] = next_G

            # # check if we need to backtrack
            # id = (keys[key], keys_id)
            # if id in best_steps and best_steps[id] <= next_steps + steps:
            #     pass # backtrack, we have found a better solution already
            # else:
            #     # add or update best solution
            #     best_steps[id] = next_steps + steps

            best = min(best, next_steps + find_keys(keys[key], tuple(next_keys_to_find)))

    return best

# approach from 18a first try
print("FK:", find_keys(start, tuple(set(keys.keys()))))

# print(min_steps)

# 3116 te hoog, 3012?

# 2946 heel lang, 10 minuten ofzo! (maar wel goed)

# 12:11
# 12:20


