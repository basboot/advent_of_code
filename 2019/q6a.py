# Using readlines()
from networkx import minimum_edge_cut, shortest_path, descendants

from tools.advent_tools import *
import networkx as nx

file1 = open('q6a.txt', 'r')
lines = file1.readlines()

G = nx.DiGraph()

you = None
san = None

for line in lines:
    to_node, from_node = line.rstrip().split(")") # from_note = center, to_node = orbitting

    # add nodes
    for node in [from_node, to_node]:
        if node not in G:
            G.add_node(from_node)
        if from_node == "YOU":
            you = to_node
        if from_node == "SAN":
            san = to_node

for line in lines:
    from_node, to_node = line.rstrip().split(")")
    # add edges
    G.add_edge(to_node, from_node)

assert you is not None and san is not None, "SAN or YOU not found"

print(G)

total = 0
for node in G.nodes():
    total += len(list(nx.ancestors(G.reverse(), node)))

print("Part 1", total)

# Create undirected graph for travel
G = nx.Graph(G)

print("Part 2", len(nx.shortest_path(G, you, san)) - 1) # path is # nodes in between - 1