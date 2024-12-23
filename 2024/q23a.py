from itertools import combinations

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

import networkx as nx
import matplotlib.pyplot as plt

# ChatGPT for drawing :-)
def draw_graph_balanced(graph, answer):
    pos = nx.spring_layout(graph)

    plt.figure(figsize=(30, 30))

    colors = ["red" if node in answer else "lightblue" for node in graph.nodes()]

    # Draw the graph
    nx.draw(
        graph, pos,
        with_labels=True,  # Include labels on the nodes
        node_color=colors,
        edge_color="gray",
        node_size=500,
        font_size=10
    )

    # Add node names explicitly (for finer control, if needed)
    labels = {node: str(node) for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_color="black")

    plt.savefig("q23.pdf", format="pdf", bbox_inches="tight")
    plt.show()

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

max_clique = sorted(list(nx.find_cliques(G)), key=len, reverse=True)[0]

print("Part 2", ",".join(sorted(max_clique)))

draw_graph_balanced(G, set(max_clique))
