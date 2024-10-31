import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q18a.txt', 'r')

program = []
registers = defaultdict(int)
sounds = [0]

for line in file1.readlines():
    data = line.rstrip().split(" ")
    command = data[0]
    parameters = data[1:]

    program.append((command, parameters))

program_counter = 0

def value(n):
    try:
        return int(n)
    except:
        return registers[n]

def play(n):
    global sounds
    sounds.append(n)

def recover(n):
    global sounds

    if n == 0:
        return # do not recover

    print("Part 1, first recover will be executed: ", sounds[-1])

    sounds.append(sounds[-1])

    exit() # Part1



def jump_greater_than_zero(n, offset):
    if n > 0:
        return offset - 1 # -1, because counter will always be incremented by one
    else:
        return 0

while True:
    command, parameters = program[program_counter]

    print(program_counter, command, parameters)

    match command:
        case "snd":
            play(value(parameters[0]))
        case "set":
            registers[parameters[0]] = value(parameters[1])
        case "add":
            registers[parameters[0]] += value(parameters[1])
        case "mul":
            registers[parameters[0]] *= value(parameters[1])
        case "mod":
            registers[parameters[0]] %= value(parameters[1])
        case "rcv":
            recover(value(parameters[0]))
        case "jgz":
            program_counter += jump_greater_than_zero(value(parameters[0]), value(parameters[1]))

    program_counter += 1







