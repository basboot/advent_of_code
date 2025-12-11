import networkx as nx
from networkx.algorithms.cycles import find_cycle
from networkx.algorithms.simple_paths import all_simple_paths

G = nx.DiGraph()

with open("q11a.txt") as f:
    for line in f:
        from_device, to_devices = line.strip().split(": ")
        to_devices = to_devices.split(" ")

        for device in to_devices:
            G.add_edge(from_device, device)



print(f"Part 1 {len(list(all_simple_paths(G, "you", "out")))}")

print(find_cycle(G))