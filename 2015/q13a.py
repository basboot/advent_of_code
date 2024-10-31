from itertools import permutations

import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.traveling_salesman import greedy_tsp

file1 = open('q13a.txt', 'r')
lines = file1.readlines()

import networkx as nx

def brute_force_max_happiness(G):
    nodes = list(G.nodes)
    shortest_path = None
    max_path_length = 0

    # Generate all permutations of nodes
    for perm in permutations(nodes):
        # Check if perm forms a valid path
        path_length = 0
        valid_path = True
        for i in range(len(perm)):
            if G.has_edge(perm[i], perm[(i + 1) % len(perm)]):
                path_length += G[perm[i]][perm[(i + 1) % len(perm)]].get('weight', 0)
            else:
                valid_path = False
                break

        # Update shortest path if valid and shorter
        if valid_path and path_length > max_path_length:
            max_path_length = path_length
            shortest_path = perm

    return shortest_path, max_path_length


G = nx.Graph()

for line in lines:
    # London to Dublin = 464
    node1, _, gainloss, value, _, _, _, _, _, _, node2 = line.rstrip().replace(".", "").split(" ")

    # print(gainloss, value)
    weight = int(value) * (1 if gainloss == "gain" else -1)
    # print(weight)

    if (node1, node2) in G.edges:
        # print("seen before, update weight")
        G.edges[(node1, node2)]["weight"] += weight
    else:
        G.add_edge(node1, node2, weight=weight)

    # print(G.edges[(node1, node2)])

print(G)

print("Part 1", brute_force_max_happiness(G))

for node in list(G.nodes):
    G.add_edge(node, "Bas", weight=0)


print(G)

print("Part 2", brute_force_max_happiness(G))