from itertools import permutations

import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.traveling_salesman import greedy_tsp

file1 = open('q9a.txt', 'r')
lines = file1.readlines()

import networkx as nx

# ChatGPT
def brute_force_shortest_path(G):
    nodes = list(G.nodes)
    shortest_path = None
    max_path_length = 0

    # Generate all permutations of nodes
    for perm in permutations(nodes):
        # Check if perm forms a valid path
        path_length = 0
        valid_path = True
        for i in range(len(perm) - 1):
            if G.has_edge(perm[i], perm[i + 1]):
                path_length += G[perm[i]][perm[i + 1]].get('weight', 1)  # Assuming weight of 1 if not provided
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
    node1, _, node2, _, distance_str = line.rstrip().split(" ")
    distance = int(distance_str)

    G.add_edge(node1, node2, weight=distance)

print(G)

path = nx.approximation.traveling_salesman_problem(G, cycle=False,method=greedy_tsp)

print(path)

total = 0
for i in range(len(path) - 1):
    print(G.edges[(path[i], path[i + 1])])
    total += G.edges[(path[i], path[i + 1])]['weight']

print("Total", total)

print(brute_force_shortest_path(G))

# 127 too high


#
# pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
#
# # nodes
# nx.draw_networkx_nodes(G, pos, node_size=700)
#
# # edges
# nx.draw_networkx_edges(G, pos, width=6)
#
# # node labels
# nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
# # edge weight labels
# edge_labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)
#
# ax = plt.gca()
# ax.margins(0.08)
# plt.axis("off")
# plt.tight_layout()
# plt.show()



