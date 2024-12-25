from collections import deque, defaultdict

import networkx as nx

import matplotlib.pyplot as plt

from pyvis.network import Network

file1 = open('q24a.txt', 'r')
lines = file1.readlines()


def plot_graph(G):
    pos = nx.kamada_kawai_layout(G)  # Balanced layout for other nodes

    for i in range(2):
        # Top row: alternating X00, Y00, X01, Y01...
        x_nodes = [node for node in G.nodes if node.startswith('x')]
        y_nodes = [node for node in G.nodes if node.startswith('y')]
        other_nodes = [node for node in G.nodes if node[0] not in {'x', 'y', 'z'}]
        x_nodes.sort()
        y_nodes.sort()
        top_row = [node for pair in zip(sorted(x_nodes), sorted(y_nodes)) for node in pair]

        if i < 0:
            for node in other_nodes:
                pos[node] = (pos[node][0], 0)

        n_top = len(top_row)
        for i, node in enumerate(top_row):
            pos[node] = ((i / (n_top - 1))*2 - 1, 1)  # Spread from left (0) to right (1) at the top

        # Bottom row: Z00 to Z45
        z_nodes = sorted([node for node in G.nodes if node.startswith('z')])
        n_bottom = len(z_nodes)
        for i, node in enumerate(z_nodes):
            pos[node] = ((i / (n_bottom - 1)) * 2 - 1, -1)  # Spread from left (0) to right (1) at the bottom

        if i < 1:
            pos = nx.kamada_kawai_layout(G, pos=pos)
    # Draw the graph
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    plt.figure(figsize=(80, 5))

    nx.draw(
        G, pos, with_labels=True,
        edge_color=edge_colors,
        node_color='lightblue',
        font_weight='bold',
        font_color='black',
        node_size=50,
        font_size=4
    )

    plt.savefig("q24.pdf", format="pdf", bbox_inches="tight")
    # plt.show()

G = nx.DiGraph()


reading_inputs = True

message_queue = deque()
gates = []

inputs1 = defaultdict(list)
inputs2 = defaultdict(list)

colors = {
    'AND': 'red',
    'OR': 'green',
    'XOR': 'blue'
}

for line in lines:
    row = line.rstrip()
    if row == "":
        reading_inputs = False
        continue

    if reading_inputs:
        destination, signal = row.split(": ")
        message_queue.append((destination, int(signal)))
    else:
        input1, operation, input2, output = row.replace("-> ", "").split(" ")

        G.add_edge(input1, output, color=colors[operation])
        G.add_edge(input2, output, color=colors[operation])

        gates.append([None, None, operation, output])

        inputs1[input1].append(len(gates) - 1)
        inputs2[input2].append(len(gates) - 1)

IN1, IN2, OP, OUT = 0, 1, 2, 3

print(message_queue)

solution = []

while len(message_queue) > 0:
    destination, signal = message_queue.popleft()
    # print("S", destination, signal)

    if destination in inputs1:
        for gate in inputs1[destination]:
            assert gates[gate][IN1] is None, "gate already received signal 1"
            gates[gate][IN1] = signal

            if gates[gate][IN2] is not None:
                match gates[gate][OP]:
                    case "AND":
                        result = gates[gate][IN1] & gates[gate][IN2]
                    case "OR":
                        result = gates[gate][IN1] | gates[gate][IN2]
                    case "XOR":
                        result = gates[gate][IN1] ^ gates[gate][IN2]
                    case _:
                        assert False, "unknown op"
                message_queue.append((gates[gate][OUT], result))

    if destination in inputs2:
        for gate in inputs2[destination]:
            assert gates[gate][IN2] is None, "gate already received signal 2"
            gates[gate][IN2] = signal

            if gates[gate][IN1] is not None:
                match gates[gate][OP]:
                    case "AND":
                        result = gates[gate][IN1] & gates[gate][IN2]
                    case "OR":
                        result = gates[gate][IN1] | gates[gate][IN2]
                    case "XOR":
                        result = gates[gate][IN1] ^ gates[gate][IN2]
                    case _:
                        assert False, "unknown op"

                message_queue.append((gates[gate][OUT], result))

    if destination[0] == 'z':
        solution.append((destination, signal))

print(solution)

print(int("".join([str(x[1]) for x in sorted(solution, reverse=True)]), 2))

wrong_outputs = ["thm", "z08", "hwq", "z22", "gbs", "z29", "wss", "wrm"]

print(f"Part 2, {','.join(sorted(wrong_outputs))}")

plot_graph(G)

nt = Network(directed=True, height='1000px')
# populates the nodes and edges data structures
nt.from_nx(G)
nt.show_buttons(['physics'])
nt.show('q24.html', notebook=False)


