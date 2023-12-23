# Using readlines()
import sys
from functools import lru_cache

from networkx import minimum_edge_cut

from tools.advent_tools import *

sys.setrecursionlimit(20000)

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

trees, width, height = read_grid(lines, GRID_SET, lambda a: a.strip(), {".": None, "<": None, ">": None, "^": None, "v": None, "#": True}, )
map, width, height = read_grid(lines, GRID_DICT, lambda a: a.strip(),  )

# obstacles
print(trees)
# add trees to close the map
start = (0, 1)
trees.add((-1, 1)) # start
goal = (height - 1, width - 2)
trees.add((height, width - 2)) # goal

ACTION_MAP = {
    ".": [NORTH, EAST, SOUTH, WEST],
    "<": [WEST],
    ">": [EAST],
    "^": [NORTH],
    "v": [SOUTH],
    "#": [] # should not be possible to land on a tree
}

# full layout
print(map)

# approach 1
# problem too large for finding all paths with dfs => divide problem in sub problems using bottlenecks in the map
# -> not working, mistake or not good enough?

# approach 2
# give each edge a weight of 1, then remove each node with only two edges, and combine the weigts of the edges

# Create graph network,
# and find min cuts
# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.cuts.minimum_edge_cut.html
import networkx as nx

G = nx.Graph()

# add nodes
for tile in map:
    if map[tile] != "#":
        G.add_node((tile))

# add edges
for tile in map:
    if map[tile] != "#":
        for action in [NORTH, EAST, SOUTH, WEST]:
            n, _ = next_pos(tile, action)
            if n not in trees:
                G.add_edge(tile, n)
                G[tile][n]["weight"] = 1 # initial weight of edge



# cut network in pieces
def cut_network(G, start, goal):
    if start == goal: # no edges left between
        return [start]
    min_cuts = minimum_edge_cut(G, s=start, t=goal)
    # print(len(min_cuts), min_cuts)
    if len(min_cuts) > 1:  # more than 1 edge needs to be cut, no more bottleneck
        return [start, goal]
    min_cuts = list(min_cuts)
    min_cut = min_cuts[0]
    assert len(min_cut) == 2, "more than 2 nodes for single edge should not be possible"
    # assume they are in order
    firs_part, last_part = min_cut
    # cut
    G.remove_edge(firs_part, last_part)

    return cut_network(G, start, firs_part) + cut_network(G, last_part, goal)

# cuts = cut_network(G, start, goal)


# longest path problem is NP-hard, so we need to brute force

# find node with only two edges, and remove it
def remove_node(G):
    for node in G.nodes():
        # print(node)

        edges = list(G.edges(node))

        if len(edges) == 2:
            # this is not a node, remove from graph
            weight1 = G.edges[edges[0]]["weight"]
            weight2 = G.edges[edges[1]]["weight"]

            # connect surrounding nodes
            before = edges[0][1]
            after = edges[1][1]

            G.add_edge(before, after)
            G[before][after]["weight"] = weight1 + weight2 # new edga has combined weight

            G.remove_node((node))
            return G, True

    return G, False # no nodes to remove

print("size before reducing", len(G))

# remove nodes until there are nog nodes with only 2 edges left
has_changed = True
while has_changed:
    G, has_changed = remove_node(G)

print("size after reducing", len(G))

@lru_cache(maxsize=10000)
def dfs(pos, goal, visited: tuple, weight) -> int:
    visited_set = set(visited)
    visited_set.add(pos)
    visited = tuple(visited_set)

    if pos == goal:
        return weight - 1 # return steps, not visits so -1

    max_len = 0


    for edge in G.edges(pos):
        # print(edge)
        next = edge[1]
        if next in visited: # never visit same tile twice (no edges to trees in graph)
            continue
        next_len = dfs(next, goal, visited, weight + G.edges[edge]["weight"])
        max_len = max(max_len, next_len)
    return max_len

total = 0

# mincut approach not working, just use the initial start and goal
cuts = [start, goal]

print(len(cuts), "cuts")
for i in range(len(cuts) - 1):
    print(f"{i + 1}. from {cuts[i]} to {cuts[i + 1]}")
    total += dfs(cuts[i], cuts[i + 1], (), 0) + 1
    print(total)


print(total)






