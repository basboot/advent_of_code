import sys

import networkx as nx

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

route = lines[0].rstrip()[1:-1] # don;t neet ^ and $

directions = {
    "N": -1,
    "E": 1j,
    "S": 1,
    "W": -1j
}

# start at 0, 0, use set to avoid doubles
positions = {0}

stack_spawnpoints: [set] = []
stack_continues: [set] = []

G = nx.Graph()

for char in list(route):
    match char:
        case '(':
            stack_spawnpoints.append(positions)
            stack_continues.append(set())
        case ')':
            # cleanup stacks
            stack_spawnpoints.pop(-1)
            positions = positions.union(stack_continues[-1])
            stack_continues.pop(-1)
        case '|':
            # store endpoint
            stack_continues[-1] = stack_continues[-1].union(positions)
            # reset to last
            positions = stack_spawnpoints[-1].copy()
        case "N" | "E" | "S" | "W":
            # walk
            next_positions = set()
            for position in positions:
                next_position = position + directions[char]
                next_positions.add(next_position)
                G.add_edge(position, next_position)
            positions = next_positions
        case _:
            assert True, "Unknown direction"

print(positions)
print(G)

shortest_paths = nx.algorithms.shortest_path_length(G, 0)
print("Part 1", max(shortest_paths.values()))

print("Part 2", len(list(filter(lambda x: x >= 1000, shortest_paths.values()))))