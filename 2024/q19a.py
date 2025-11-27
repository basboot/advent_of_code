from collections import defaultdict
from functools import cache

file1 = open('q19a.txt', 'r')
lines = file1.readlines()


towels = lines[0].rstrip().split(", ")
patterns = []
for line in lines[2:]:
    patterns.append(line.rstrip())

towel_patterns = defaultdict(list)

for towel in towels:
    towel_patterns[towel[0]].append(towel)

print(towels)
print(towel_patterns)

def is_possible(pattern, pos):
    if pos >= len(pattern):
        return True

    for towel_pattern in towel_patterns[pattern[pos]]:
        if len(towel_pattern) > len(pattern) - pos:
            continue
        else:
            if towel_pattern == pattern[pos: pos + len(towel_pattern)]:
                if is_possible(pattern, pos + len(towel_pattern)):
                    return True
    return False

@cache
def count_possible(pattern, pos):
    if pos >= len(pattern):
        return 1

    n_possible = 0
    for towel_pattern in towel_patterns[pattern[pos]]:
        if len(towel_pattern) > len(pattern) - pos:
            continue
        else:
            if towel_pattern == pattern[pos: pos + len(towel_pattern)]:
                n_possible += count_possible(pattern, pos + len(towel_pattern))

    return n_possible

total = 0
total2 = 0


for pattern in patterns:

    possible = is_possible(pattern, 0)
    n_possible = count_possible(pattern, 0)
    # print(pattern, possible, n_possible)
    if possible:
        total += 1
    total2 += n_possible
print(total, total2)


