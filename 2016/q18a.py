file1 = open('q18a.txt', 'r')

traps = set()

map = list(file1.readlines()[0].rstrip())
rows = 400000 # Part 1 40

for j, value in enumerate(map):
    if value == '^':
        traps.add((0, j))


for i in range(1, rows):
    for j in range(len(map)):
        left = (i-1, j-1) in traps
        center = (i-1, j) in traps
        right = (i-1, j+1) in traps

        if left != right:
            traps.add((i, j))


print("Part 1/2", len(map) * rows - len(traps))

