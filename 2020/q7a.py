from networkx import ancestors

file1 = open('q7a.txt', 'r')
lines = file1.readlines()

import networkx as nx
G = nx.DiGraph()

# create all nodes
for line in lines:
    row = line.rstrip().replace(".", "").split(" contain ")

    container = row[0][:-5]
    G.add_node(container)

    if row[1][0:2] != "no":
        contains = row[1].split(", ")
        for bags in contains:
            number = int(bags.split(" ")[0])
            design = " ".join(bags.split(" ")[1:-1])
            G.add_node(design)

# add all edges
for line in lines:
    row = line.rstrip().replace(".", "").split(" contain ")

    container = row[0][:-5]

    if row[1][0:2] != "no":
        contains = row[1].split(", ")
        for bags in contains:
            number = int(bags.split(" ")[0])
            design = " ".join(bags.split(" ")[1:-1])
            G.add_edge(container, design, capacity=number)

print(G)


print("Part 1", len(ancestors(G, "shiny gold")))

start = "shiny gold"

def count_bags(bag):
    n_bags = 1 # self

    # + children * capacity
    for edge in G.out_edges(bag):
        n = nx.get_edge_attributes(G, "capacity")[edge]
        next_node = edge[1]

        n_bags += n * count_bags(next_node)

    return n_bags

print("Part 2", count_bags(start) - 1) # -1, don't count gold bag itself


