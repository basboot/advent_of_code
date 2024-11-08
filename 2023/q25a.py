# Using readlines()
import networkx as nx
from networkx import minimum_edge_cut, descendants

file1 = open('q25a.txt', 'r')
lines = file1.readlines()

G = nx.Graph()

for line in lines:
    from_node, to_nodes = line.rstrip().split(": ")
    to_nodes = to_nodes.split(" ")

    # add nodes
    for node in [from_node] + to_nodes:
        if node not in G:
            G.add_node(from_node)

for line in lines:
    from_node, to_nodes = line.rstrip().split(": ")
    to_nodes = to_nodes.split(" ")

    # add edges
    for to_node in to_nodes:
        G.add_edge(from_node, to_node)

print(G)

# find min cut
min_cuts = minimum_edge_cut(G)
assert len(list(min_cuts)) == 3, "Mincut not equal to 3 edges, as stated in assignment"

# make the cut
left = right = None
for edge in list(min_cuts):
    print(edge)
    G.remove_edge(edge[0], edge[1])
    left = edge[0]
    right = edge[1]

#  count number of reachable nodes on both sides of the cut
left_d = descendants(G, left)
right_d = descendants(G, right)

# add one to the descendants, because the node itself is also part of the partition
print("Total", (len(left_d) + 1) * (len(right_d) + 1))

