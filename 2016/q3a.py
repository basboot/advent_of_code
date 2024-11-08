file1 = open('q3a.txt', 'r')
lines = file1.readlines()

possible = 0

for line in lines:
    a, b, c = sorted([int(x) for x in line.rstrip().replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")[1:]])

    if a + b > c:
        possible += 1

print("Part 1", possible)

possible = 0

for i in range(0, len(lines), 3):
    for j in range(3):
        a, b, c = sorted([int(lines[i].rstrip().replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")[1:][j]), int(lines[i+1].rstrip().replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")[1:][j]), int(lines[i+2].rstrip().replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")[1:][j])])

        if a + b > c:
            possible += 1

print("Part 2", possible)
