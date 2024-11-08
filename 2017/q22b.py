file1 = open('q22a.txt', 'r')
lines = file1.readlines()

grid = {} # keeps only locations (as complex number) and state of infected/weakened and flagged nodes

for i in range(len(lines)):
    line = lines[i].rstrip()
    for j in range(len(line)):
        if line[j] == "#":
            grid[i + j*1j] = "infected"

middle = len(lines) // 2

current_node = middle + middle * 1j
direction = -1

print(current_node)

print(direction) # turn left *1j, turn right *-1j

infected = 0

for _ in range(10000000):
    # infected? turn right, not infected turn left

    if current_node in grid:
        state = grid[current_node]
    else:
        state = "clean"

    match state:
        case "clean":
            direction *= 1j
            grid[current_node] = "weakened"
        case "weakened":
            infected += 1
            grid[current_node] = "infected"
        case "infected":
            direction *= -1j
            grid[current_node] = "flagged"
        case "flagged":
            direction *= -1
            del grid[current_node]

    current_node += direction



print(infected)
