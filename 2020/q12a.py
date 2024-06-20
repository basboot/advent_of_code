from tools.advent_tools import *

file1 = open('q12a.txt', 'r')
lines = file1.readlines()

instructions = []
for line in lines:
    row = line.rstrip()

    instructions.append((row[0], int(row[1:])))


print(instructions)

orientation = EAST
pos = (0, 0)

for instruction, value in instructions:
    match instruction:
        case "N":
            pos, _ = next_pos(pos, NORTH, steps=value)
        case "E":
            pos, _ = next_pos(pos, EAST, steps=value)
        case "S":
            pos, _ = next_pos(pos, SOUTH, steps=value)
        case "W":
            pos, _ = next_pos(pos, WEST, steps=value)
        case "L":
            orientation = (orientation - (value // 90)) % 4
        case "R":
            orientation = (orientation + (value // 90)) % 4
        case "F":
            pos, _ = next_pos(pos, orientation, steps=value)

print("Part 1", pos[0] + pos[1])