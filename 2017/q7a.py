from collections import Counter

import numpy as np

import networkx as nx
G = nx.DiGraph()

file1 = open('q7a.txt', 'r')
lines = file1.readlines()

weights = {}

for line in lines:
    nodes = line.rstrip().split(" -> ")

    node, weight = nodes[0].replace("(", "").replace(")", "").split(" ")
    weights[node] = int(weight) # store weights in dict (could also be stored in networkx... if you look up how ;-)

    children = nodes[1].split(", ") if len(nodes) > 1 else []

    for child in children:
        G.add_edge(node, child)

root = list(nx.topological_sort(G))[0]

def dfs(node):
    child_weights = []
    for child in G.neighbors(node):
        child_weights.append(dfs(child))

    if len(set(child_weights)) > 1:
        print("Problem found")
        print(list(G.neighbors(node)))
        print(child_weights)

        print("wrong weight", 2166 - 2159)
        print(weights['vrgxe'])

        print("needs to be")
        print(weights['vrgxe'] - (2166 - 2159))

        exit()

    return weights[node] + sum(child_weights)

print(dfs(root))



