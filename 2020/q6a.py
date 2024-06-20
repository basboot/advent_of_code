file1 = open('q6a.txt', 'r')
lines = file1.readlines()

groups = []
group = set()

for line in lines:
    row = line.rstrip()

    if row == "":
        groups.append(group)
        group = set()
        continue

    answers = [x for x in row]
    for answer in answers:
        group.add(answer)

groups.append(group)

print(groups)

print("Part 1", sum([len(x) for x in groups]))

