import itertools

from mip import *

file1 = open('q17a.txt', 'r')
lines = file1.readlines()

liters = 150

sizes = []
for line in lines:
    sizes.append(int(line.rstrip()))

total = 0

solutions = defaultdict(int)

for buckets in range(len(sizes) + 1):
    for combination in itertools.combinations(sizes, buckets):
        if sum(combination) == liters:
            total += 1
            solutions[buckets] += 1


print("Part 1", total)

print("Part 2", solutions[min(list(solutions.keys()))])