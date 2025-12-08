import math
import numpy as np
import re

assignments = []
with open("q6a.txt") as f:
    for line in f:
        assignments.append(f"{line.replace("\n","")}")

# add spaces at end to align rows, to change to numpy array
longest = max(len(line) for line in assignments)
assignments = np.array([list(line.ljust(longest)) for line in assignments])

assignment = []
total = 0
for j in range(len(assignments[-1]) - 1, -1, -1): # work right to left because operators are on the left
    col = re.sub(r"\s+", "", "".join(assignments[:-1, j])) # join column values, remove spaces
    if col == "": # no numbers in column is separator, reset assignment
        assignment = []
        continue
    assignment.append(int(col)) # add number to assignment
    if assignments[-1, j] != " ": # operator ends assignment, calc assignment
        total += sum(assignment) if assignments[-1, j] == "+" else math.prod(assignment)

print(f"Part 2: {total}")

