import networkx as nx
G = nx.Graph()

file1 = open('q12a.txt', 'r')
lines = file1.readlines()


for line in lines:
    source, sinks = line.rstrip().split(" <-> ")
    for sink in sinks.split(", "):
        G.add_edge(source, sink)


print("Part 1", len(nx.node_connected_component(G, "0")))
print("Part 2", len(list(nx.connected_components(G))))