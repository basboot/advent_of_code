import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q24a.txt', 'r')

ports = []

port_lookup = defaultdict(list)

for line in file1.readlines():
    pins1, pins2 = [int(x) for x in line.rstrip().split("/")]
    ports.append((pins1, pins2))

    port_lookup[pins1].append((len(ports) - 1, pins2))
    port_lookup[pins2].append((len(ports) - 1, pins1))



# print(port_lookup)

strengths = []

def create_bridge(pins_in, used_ports):
    global strengths
    optional_parts = port_lookup[pins_in]

    for part_id, pins_out in optional_parts:
        if part_id in used_ports:
            continue # cannot use parts twice
        new_used_parts = used_ports.copy()
        new_used_parts.add(part_id)

        create_bridge(pins_out, new_used_parts)

    strength = 0
    for port in used_ports:
        # print(ports[port], end="-")
        strength += ports[port][0] + ports[port][1]

    # print("=", strength)
    strengths.append((strength, len(used_ports)))

create_bridge(0, set())

print("Part 1", max(strengths))

strengths.sort(key = lambda x: (x[1], x[0]), reverse=True)

print("Part 2", strengths[0])

print(strengths[0:30])

# 1772 too low