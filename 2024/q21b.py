import math
import time
from functools import cache

from networkx.algorithms.shortest_paths.generic import all_shortest_paths

file1 = open('q21.txt', 'r')
lines = file1.readlines()

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

@cache
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

MAX_DEPTH = 25

robot_cache = {}

def find_all_shortest_paths(sequence, last_key=None, depth=0):
    n_steps = 0
    last_key_next_step = None
    for i in range(len(sequence)):
        if (last_key, sequence[i], depth) in robot_cache:
            last_key_next_step, n_steps_next = robot_cache[(last_key, sequence[i], depth)]
        else:
            shortest_steps = paths_to_key(last_key if last_key is not None else 'A', sequence[i], NUMERIC if depth == 0 else DIRECTIONAL)

            # at last robot, just return the first best result
            if depth == MAX_DEPTH:
                last_key_next_step, n_steps_next = shortest_steps[0][-1], len(shortest_steps[0])
            # other robots need to check what is best for the next robot
            else:
                n_steps_next = math.inf
                for shortest_step in shortest_steps:
                    # add last key from previous result
                    last_key_next_step_result, n_steps_next_result = find_all_shortest_paths(shortest_step, last_key_next_step, depth + 1)
                    if n_steps_next_result < n_steps_next:
                        last_key_next_step = last_key_next_step_result
                        n_steps_next = n_steps_next_result

            robot_cache[(last_key, sequence[i], depth)] = last_key_next_step, n_steps_next

        last_key = sequence[i]

        n_steps += n_steps_next
    return last_key, n_steps


start_time = time.time()

total = 0
for code in codes:
    sps = find_all_shortest_paths(code)

    n_keys = sps[1]
    n_code = int(code[:-1])

    print(f"{n_keys} x {n_code} = {n_keys * n_code}")

    total += n_keys * n_code

print(total)
print(time.time() - start_time)


# 4.2187910079956055
# 0.0006902217864990234