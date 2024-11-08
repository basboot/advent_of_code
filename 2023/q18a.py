# Using readlines()
import queue

from tools.advent_tools import *

file1 = open('q18a.txt', 'r')
lines = file1.readlines()


digging, width, height = read_grid(lines, GRID_LIST, lambda a: a.strip().replace("(","").replace(")","").replace("#","").split(" "))

print(digging)

DIR_TO_WIND = {
    "U": NORTH,
    "R": EAST,
    "D": SOUTH,
    "L" : WEST
}

def dig_interior(pos):
    global hole

    to_dig = queue.Queue()

    to_dig.put(pos)

    dig_set = set()


    while not to_dig.empty() > 0:
        pos = to_dig.get()
        i, j = pos

        hole.add(pos)

        if len(hole) % 1000 == 0:
            print(len(hole))

        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == dj:
                    continue
                next_pos = i + di, j + dj

                if next_pos not in dig_set and next_pos not in hole:
                    to_dig.put(next_pos)
                    dig_set.add(next_pos)




pos = (0, 0)
hole = {(0, 0)}
for dig in digging:
    direction, length, color = dig
    for i in range(int(length)):
        pos, _ = next_pos(pos, DIR_TO_WIND[direction])
        hole.add(pos)

print(len(hole))

# TODO: check assumption whole is always right and below
dig_interior((1, 1))

print(len(hole))

