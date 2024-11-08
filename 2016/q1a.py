file1 = open('q1a.txt', 'r')
lines = file1.readlines()

position = 0
direction = 1

visited = {0}

for turn, steps in [(-1j if x[0] == 'R' else 1j, int(x[1:])) for x in lines[0].rstrip().split(", ")]:
    direction *= turn
    for _ in range(steps):
        position += (direction * 1)
    # print(position)

        if position in visited:
            print("Part 2", abs(position.real) + abs(position.imag))
        visited.add(position)

print("Part 1", abs(position.real) + abs(position.imag))