import math
from collections import defaultdict

import numpy as np

file1 = open('q2a.txt', 'r')
lines: [str] = file1.readlines()

def count_errors(current: int, report: [int]) -> int:
    # end of report, so no more errors
    if current >= len(report):
        return 0

    # first is always safe
    # no previous is always safe
    # in range is safe if it's the first interval, or of it has the same sign as the previous interval
    if current == 0 or (0 < abs(report[current] - report[current - 1]) < 4 and (current == 1 or np.sign(report[current] - report[current - 1]) == np.sign(report[current - 1] - report[current - 2]))):
        return count_errors(current + 1, report)
    else:
        # if not safe, problem can be this number, the previous number, and even the one before (if it is the first it might change inc/dec)
        # try all three, and use best
        return 1 + min(count_errors(0, [report[i] for i in range(len(report)) if i != current]), count_errors(0, [report[i] for i in range(len(report)) if i != current - 1]) if current > 0 else math.inf, count_errors(0, [report[i] for i in range(len(report)) if i != current - 2]) if current > 1 else math.inf)

errors = defaultdict(int)

for line in lines:
    report: [int] = [int(x) for x in line.rstrip().split()]
    errors[count_errors(0, report)] += 1

print(f"Part 1: {errors[0]}")
print(f"Part 2: {errors[0] + errors[1]}")