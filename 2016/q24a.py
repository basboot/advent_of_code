import math

import networkx as nx
from networkx.algorithms.approximation.traveling_salesman import traveling_salesman_problem, greedy_tsp, \
    simulated_annealing_tsp

file1 = open('q24a.txt', 'r')

lines = file1.readlines()

max_i = -math.inf
max_j = -math.inf
reachable = set()
targets = set()
zero = None
for i, line in enumerate(lines):
    max_i = max(i, max_i)
    for j, c in enumerate(list(line.rstrip())):
        max_j = max(j, max_j)
        match c:
            case "#":
                continue
            case ".":
                reachable.add((i, j))
            case "0":
                reachable.add((i, j))
                targets.add((i, j))
                zero = (i, j)
            case _:
                reachable.add((i, j))
                targets.add((i, j))

print(reachable)

G = nx.Graph()

for i in range(max_i):
    for j in range(max_j):
        if (i, j) not in reachable:
            continue

        for di, dj in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            ni, nj = i + di, j + dj
            if (ni, nj) in reachable:
                print("Create edge")
                G.add_edge((i, j), (ni, nj))

print(G)



# Part 1
print(len(traveling_salesman_problem(G, nodes=targets, cycle=False, method=lambda G, wt: greedy_tsp(G, source=zero))) - 1)


# Part 2
# tsp = traveling_salesman_problem(G, nodes=targets, cycle=True, method=lambda G, wt: greedy_tsp(G, source=zero))
tsp = traveling_salesman_problem(G, nodes=targets, cycle=True, method=lambda G, wt: simulated_annealing_tsp(G, "greedy", source=zero))
# tsp = traveling_salesman_problem(G, nodes=targets, cycle=True) # christofides default, start not needed for cycle of course

print(len(tsp) - 1)

# greedy 712
# simulated annealing 704
# christofides 712