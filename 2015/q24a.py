import itertools
from math import prod

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

packets = []
for line in lines:
    packets.append(int(line.rstrip()))

print(packets)


def all_legal_splits(packets):
    results = []
    for permutation in itertools.permutations(packets):
        # print(permutation)
        n = len(packets)

        for i in range(1, n):
            for j in range(i + 1, n):
                # group 1 must be largest
                if i > n // 3:
                    continue
                # Split the list based on combinations of indices
                group1 = permutation[:i]
                group2 = permutation[i:j]
                group3 = permutation[j:]

                if sum(group1) == sum(group2) and sum(group2) == sum(group3):
                    split = [len(group1), prod(group1), group1, group2, group3]
                    results.append(split)

    return results


all_possible_splits = all_legal_splits(packets)

all_possible_splits.sort()

print("created splits")

print("Part 1", all_possible_splits[0])


print(len(all_possible_splits))

