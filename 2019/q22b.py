# Using readlines()
from functools import cache


from lagrange import lagrange

from networkx import shortest_path

from tools.advent_tools import *

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

CARD_TO_FOLLOW = 2020

DECK_SIZE = 119315717514047
ITERATIONS = 101741582076661

position = CARD_TO_FOLLOW


@cache
def next_pos(position, reverse=False):
    for i in range(len(lines)) if not reverse else range(len(lines) - 1, -1, -1):
        line = lines[i]
        command = line.rstrip()

        if command == "deal into new stack":
            position = DECK_SIZE - position - 1
        else:
            splitted_command = command.split(" ")
            value = int(splitted_command[-1])
            if splitted_command[0] == "cut":
                position = (position + value + DECK_SIZE) % DECK_SIZE

            if splitted_command[0] == "deal":
               # position = (position * value) % DECK_SIZE
               position = pow(value, -1, DECK_SIZE) * position % DECK_SIZE

    return position


Y = next_pos(position, True)
Z = next_pos(Y, True)
A = (Y-Z) * pow(position-Y, -1, DECK_SIZE)
B = (Y-A*position) % DECK_SIZE
print(A, B)


pos = (pow(A, ITERATIONS, DECK_SIZE) * CARD_TO_FOLLOW + B * (pow(A, ITERATIONS, DECK_SIZE) - 1) * pow(A - 1, -1, DECK_SIZE)) % DECK_SIZE

print(pos)

# 16711626764828 too low
# 33996494047632

# 98461321956136 goed