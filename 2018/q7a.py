import math
from collections import Counter
import numpy as np

file1 = open('q7a.txt', 'r')

steps = {}

for line in file1:
    first_step, next_step = line.rstrip().replace("Step ", "").replace(" can begin.", "").split(" must be finished before step ")
    if first_step not in steps:
        steps[first_step] = set()
    if next_step not in steps:
        steps[next_step] = set()

    steps[next_step].add(first_step)

def get_next():
    next_steps = sorted(list(steps.keys()), key=lambda k: (len(steps[k]), k))

    if len(next_steps) == 0:
        return None
    else:
        assert len(steps[next_steps[0]]) == 0, "We cannot take the next step"
        return next_steps[0]

while True:
    step = get_next()
    if step is None:
        break

    print(step, end="")
    del steps[step]

    for key in steps:
        if step in steps[key]:
            steps[key].remove(step)

print()