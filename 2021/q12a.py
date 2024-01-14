# Using readlines()
from networkx import minimum_edge_cut, shortest_path, descendants, all_neighbors

from tools.advent_tools import *
import networkx as nx

file1 = open('q12a.txt', 'r')
lines = file1.readlines()

G = nx.Graph()

for line in lines:
    from_node, to_node = line.rstrip().split("-")

    # add nodes
    for node in [from_node, to_node]:
        if node not in G:
            G.add_node(from_node)

for line in lines:
    from_node, to_node = line.rstrip().split("-")

    # add edges
    G.add_edge(from_node, to_node)

print(G)

def dfs(position, visited, goal):

    if position == goal:
        return 1

    if position.islower(): # don't revisit small caves
        visited.add(position)

    n_paths = 0
    for neighbour in all_neighbors(G, position):
        # print(neighbour)
        if neighbour not in visited:
            new_visited = visited.copy()
            n_paths += dfs(neighbour, new_visited, goal)

    return n_paths




start = "start"
goal = "end"


print(dfs(start, {"start"}, goal))


#