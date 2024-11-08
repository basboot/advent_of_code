import math

from tools.advent_tools import *


# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    angle = (angle * math.pi) / 180

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

file1 = open('q12a.txt', 'r')
lines = file1.readlines()

instructions = []
for line in lines:
    row = line.rstrip()

    instructions.append((row[0], int(row[1:])))


print(instructions)

orientation = EAST
pos = (0, 0)
waypoint_pos = (-1, 10)

print(">", pos, waypoint_pos)

for instruction, value in instructions:
    match instruction:
        case "N":
            waypoint_pos, _ = next_pos(waypoint_pos, NORTH, steps=value)
        case "E":
            waypoint_pos, _ = next_pos(waypoint_pos, EAST, steps=value)
        case "S":
            waypoint_pos, _ = next_pos(waypoint_pos, SOUTH, steps=value)
        case "W":
            waypoint_pos, _ = next_pos(waypoint_pos, WEST, steps=value)
        case "L":
            waypoint_pos = rotate((0, 0), waypoint_pos, +value) # around origin, not around ship
        case "R":
            waypoint_pos = rotate((0, 0), waypoint_pos, -value)
        case "F":
            di = (waypoint_pos[0] ) * value # from origin offset
            dj = (waypoint_pos[1] ) * value

            print("D", di, dj)

            pos = pos[0] + di, pos[1] + dj

    print(instruction, value)
    print(">", pos, waypoint_pos)

print("Part 1", pos[0] + pos[1])