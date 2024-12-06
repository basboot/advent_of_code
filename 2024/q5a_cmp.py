import functools
from collections import defaultdict

file1 = open('q5a.txt', 'r')
lines = file1.readlines()

before = defaultdict(set)
updates = []

read_ordering = True

for line in lines:
    row = line.rstrip()

    # newline separates page ordering and page ranges
    if row == "":
        read_ordering = False
        continue

    if read_ordering:
        left, right = row.split("|")
        before[int(right)].add(int(left))
    else:
        updates.append([int(x) for x in row.split(",")])


ranges = [[], []]
for update in updates:
    sorted_update = sorted(update, key=functools.cmp_to_key(lambda x, y: -1 if x in before[y] else 1))
    ranges[0 if update == sorted_update else 1].append(sorted_update)

print(f"Part 1, 2: {[(sum(page_range[len(page_range) // 2] for page_range in range)) for range in ranges]}")
