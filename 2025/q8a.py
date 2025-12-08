import math

import networkx as nx
import numpy as np
from networkx.algorithms.components import is_connected
from scipy.spatial.distance import cdist

junction_boxes = []
G = nx.Graph()

with open("q8a.txt") as f:
    for line in f:
        junction_box = tuple(list(map(int, line.strip().split(","))))
        junction_boxes.append(junction_box)
        G.add_node(junction_box) # add all nodes (needed for part 2)

distance_matrix = np.array(cdist(junction_boxes, junction_boxes, metric='euclidean'))

size = len(distance_matrix)

# extract only upper triangle (remove redundant symmetric distances)
closest = []
for i in range(size):
    for j in range(i + 1, size):
        distance = distance_matrix[i, j]
        closest.append((i, j, distance, tuple(junction_boxes[i]), tuple(junction_boxes[j])))

closest.sort(key=lambda x: x[2])

MAX_CONNECTIONS = 1000

connections = 0
for id_from, id_to, distance, junction_box_from, junction_box_to in closest:
    G.add_edge(junction_box_from, junction_box_to)
    connections += 1
    if connections == MAX_CONNECTIONS:
        component_sizes = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]

        print(f"Part 1: {math.prod(component_sizes[0:3])}")

    if is_connected(G):
        print(f"Part 2: {junction_box_from[0] * junction_box_to[0]}")
        break