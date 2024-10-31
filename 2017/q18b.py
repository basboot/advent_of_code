import math
from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q18a.txt', 'r')

program = []

for line in file1.readlines():
    data = line.rstrip().split(" ")
    command = data[0]
    parameters = data[1:]

    program.append((command, parameters))

bus = [[], []]

class Process:

    def __init__(self, id):
        self.program = program
        self.registers = defaultdict(int)
        self.sounds = [0]
        self.n_send = 0
        self.program_counter = 0

        self.id = id
        print("Init process", id)
        self.registers["p"] = id
        print(self.registers)

    def value(self, n):
        try:
            return int(n)
        except:
            return self.registers[n]

    def send(self, n):
        self.n_send += 1
        bus[(self.id + 1) % 2].append(n)

    def receive(self):

        if len(bus[self.id]) > 0:
            return bus[self.id].pop(0)
        else:
            return None

    def jump_greater_than_zero(self, n, offset):
        if n > 0:
            return offset - 1 # -1, because counter will always be incremented by one
        else:
            return 0

    def run(self):
        while True:
            command, parameters = self.program[self.program_counter]

            print(self.id, self.program_counter, command, parameters, self.registers)

            match command:
                case "snd":
                    self.send(self.value(parameters[0]))
                case "set":
                    self.registers[parameters[0]] = self.value(parameters[1])
                case "add":
                    self.registers[parameters[0]] += self.value(parameters[1])
                case "mul":
                    self.registers[parameters[0]] *= self.value(parameters[1])
                case "mod":
                    self.registers[parameters[0]] %= self.value(parameters[1])
                case "rcv":
                    message = self.receive()
                    if message is not None:
                        self.registers[parameters[0]] = message
                    else:
                        return
                case "jgz":
                    self.program_counter += self.jump_greater_than_zero(self.value(parameters[0]), self.value(parameters[1]))

            self.program_counter += 1


processes = [Process(0), Process(1)]

# init with first
processes[0].run()
active_process = 1

while len(bus[active_process]) > 0:
    processes[active_process].run()
    active_process = (active_process + 1) % 2

print(bus)

print("Part 2", processes[1].n_send)


