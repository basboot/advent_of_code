import time
from itertools import product

from networkx.algorithms.shortest_paths.generic import all_shortest_paths

file1 = open('q21.txt', 'r')
lines = file1.readlines()
from networkx import shortest_path

import networkx as nx

codes = []
for line in lines:
    codes.append(line.rstrip())

numerical_pad = """789
456
123
 0A"""

directional_pad = """ ^A
<v>"""

def string_to_graph(s):
    nodes = {}
    keys = {}
    for i, row in enumerate(s.split("\n")):
        for j, value in enumerate(list(row)):
            if value != " ":
                nodes[(i, j)] = value
                keys[value] = (i, j)
    G = nx.DiGraph()
    for node, value in nodes.items():
        i, j = node
        for di, dj, direction in [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]:
            ni, nj = i + di, j + dj
            if (ni, nj) in nodes:
                G.add_edge((i, j), (ni, nj), label=direction)
    return G, keys

numerical_graph, numerical_keys = string_to_graph(numerical_pad)
directional_graph, directional_keys = string_to_graph(directional_pad)

NUMERIC, DIRECTIONAL = 0, 1

def paths_to_key(start, goal, keyboard_type):
    if keyboard_type == NUMERIC:
        graph = numerical_graph
        keys = numerical_keys
    else:
        graph = directional_graph
        keys = directional_keys

    all_shortest = all_shortest_paths(graph, source=keys[start], target=keys[goal])
    presses = []
    for shortest in all_shortest:
        press = [graph.edges[(shortest[i], shortest[i+1])]['label'] for i in range(len(shortest)-1)]
        press.append('A') # always use activate
        presses.append("".join(press))
    return presses

def filter_shortest_paths(paths):
    res = min(paths, key=len)
    return list(filter(lambda x: len(x) == len(res), paths))

def find_all_shortest_paths(sequence, keyboard_type):
    s = 'A' + sequence  # always start at A
    steps = []
    for i in range(len(s) - 1):
        steps.append(paths_to_key(s[i], s[i + 1], keyboard_type))

    return ["".join(x) for x in list(product(*steps))]


start_time = time.time()
total = 0
for code in codes:
    sps = find_all_shortest_paths(code, NUMERIC)

    for _ in range(2):
        sps_next = []
        for sp in sps:
            sps_next += find_all_shortest_paths(sp, DIRECTIONAL)

        sps = filter_shortest_paths(sps_next)


    n_keys = len(sps[0])
    n_code = int(code[:-1])

    print(f"{n_keys} x {n_code} = {n_keys * n_code}")

    total += n_keys * n_code

print(total)
print(time.time() - start_time)


