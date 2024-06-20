from scipy.spatial.distance import cityblock

file1 = open('q3a.txt', 'r')
lines = file1.readlines()

wire1 = lines[0].rstrip().split(",")
wire2 = lines[1].rstrip().split(",")

# print(wire1, wire2)

# naive apprach, walk through set to mark first wire, walk again and mark all points in the set, use cityblock to sort

DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

current = (0, 0)
current_steps = 0
wires = {current: 0}

for direction, steps in [(x[0], int(x[1:])) for x in wire1]:
    for _ in range(steps):
        i, j = current
        current_steps += 1
        di, dj = DIRECTIONS[direction]
        current = (i + di, j + dj)
        wires[current] = current_steps

# print(wires)
intersections = set()
intersection_steps = {}
current = (0, 0) # skip origin
current_steps = 0

for direction, steps in [(x[0], int(x[1:])) for x in wire2]:
    for _ in range(steps):
        i, j = current
        current_steps += 1
        di, dj = DIRECTIONS[direction]
        current = (i + di, j + dj)
        if current in wires:
            intersections.add(current)

            total_steps = current_steps + wires[current]
            if current not in intersection_steps:
                intersection_steps[current] = total_steps

distances = sorted([cityblock((0, 0), x) for x in intersections])

print(distances)

print("Part 1", distances[0])

print("Part 2", sorted(intersection_steps.values())[0])