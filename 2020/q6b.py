file1 = open('q6a.txt', 'r')
lines = file1.readlines()

groups = []
group = set()
first = True

for line in lines:
    row = line.rstrip()

    if row == "":
        groups.append(group)
        group = set()
        first = True
        continue

    answers = set([x for x in row])
    if first:
        first = False
        group = group.union(answers)
    else:
        group = group.intersection(answers)

groups.append(group)

print(groups)

print("Part 1", sum([len(x) for x in groups]))

