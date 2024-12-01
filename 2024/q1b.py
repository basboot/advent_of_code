from collections import Counter

file1 = open('q1a.txt', 'r')
lines = file1.readlines()

lists = [[], []]

for line in lines:
    for i, n in enumerate([int(x) for x in line.rstrip().split("   ")]):
        lists[i].append(n)

# count number frequencies in second list
counts = Counter(lists[1])

# sum up multiplication of all numbers in first list with their frequency in second list
total = sum([n * counts[n] for n in lists[0]])

print(f"Part 2, similarity score = {total}")
