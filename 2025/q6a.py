import math
import numpy as np

assignments = []
with open("q6a.txt") as f:
    for line in f:
        assignments.append(line.strip().split())

assignments = np.array(assignments)

total = 0
for j, operation in enumerate(assignments[-1]):
    total += sum(map(int, assignments[:-1, j])) if operation == "+" else math.prod(map(int, assignments[:-1, j]))

print(f"Part 1: {total}")