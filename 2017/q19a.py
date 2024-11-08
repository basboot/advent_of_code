file1 = open('q19a.txt', 'r')
lines = file1.readlines()

diagram = {}
start = None

for i in range(len(lines)):
    line = lines[i].rstrip()
    for j in range(len(line)):
        char = line[j]

        if char != " ":
            diagram[(i, j)] = char

        if char == "|" and i == 0:
            start = (i, j)

print(diagram)
print(start)

directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

current_direction = 0
current_position = start

def next_position(position, direction):
    i, j = position
    di, dj = directions[direction]

    return i + di, j + dj

solution = []

count_steps = 0
while True:
    # walk until +
    while diagram[current_position] != "+":
        count_steps += 1
        print(current_position, current_direction)
        if diagram[current_position] not in {'-', '|'}:
            solution.append(diagram[current_position])
        current_position = next_position(current_position, current_direction)

        if current_position not in diagram:
            print("end")
            print(current_position, "".join(solution), count_steps)
            exit()

    count_steps += 1
    # try to turn
    # TODO: will fail if there are invalid symbols
    end = True
    for i in range(4): # no return
        if i == 2:
            continue # no reverse
        if next_position(current_position, (current_direction + i) % 4) in diagram:
            end = False
            current_direction = (current_direction + i) % 4
            current_position = next_position(current_position, current_direction)
            break

    if end:
        break


print(current_position, solution)



