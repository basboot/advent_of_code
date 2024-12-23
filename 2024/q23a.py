from itertools import combinations

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

import networkx as nx

G = nx.Graph()

for line in lines:
    comp1, comp2 = line.rstrip().split("-")
    G.add_edge(comp1, comp2)

total = 0
inter_connected_computers = []
for clique in nx.find_cliques(G):
    if len(clique) == 3:
        inter_connected_computers.append(sorted(clique))

    if len(clique) > 3:
        for sub_clique in combinations(clique, 3):
            inter_connected_computers.append(sorted(sub_clique))


results = set()
for computers in inter_connected_computers:

    found_t = False
    for computer in computers:
        if computer[0] == 't':
            results.add(tuple(computers))


print(f"Part 1, {len(results)}")

print("Part 2", ",".join(sorted(sorted(list(nx.find_cliques(G)), key=len, reverse=True)[0])))
