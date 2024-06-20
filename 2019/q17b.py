import math
from itertools import permutations

import numpy as np

file1 = open('q17a.txt', 'r')
lines = file1.readlines()

from tools.advent_tools import *

class Intcode:

    def __copy__(self):
        intcode_copy = Intcode(self.memory.copy(), self.inputs.copy(), self.halt_on_output)
        intcode_copy.jmp = self.jmp
        intcode_copy.instruction_pointer = self.instruction_pointer
        intcode_copy.relative_base = self.relative_base
        intcode_copy.outputs = self.outputs.copy()
        intcode_copy.extra_memory = self.extra_memory.copy()

        return intcode_copy

    def __init__(self, memory, inputs, halt_on_output = False):
        self.halt_on_output = halt_on_output
        self.jmp = None
        self.memory = memory
        self.instruction_pointer = 0
        self.relative_base = 0
        self.inputs = inputs
        self.outputs = []
        self.extra_memory = {}


        self.instructions = {
    1 : {
        "execute": lambda x: x[0] + x[1],
        "n_params": 2,
        "n_values": 4
    },
    2 : {
        "execute": lambda x: x[0] * x[1],
        "n_params": 2,
        "n_values": 4
    },
    3: {
        "execute": self.input,
        "n_params": 0,
        "n_values": 2
    },
    4: {
        "execute": self.output,
        "n_params": 1,
        "n_values": 2
    },
    5: {
        "execute": self.jump_if_true,
        "n_params": 2,
        "n_values": 3
    },
    6: {
        "execute": self.jump_if_false,
        "n_params": 2,
        "n_values": 3
    },
    7: {
        "execute": lambda x: 1 if x[0] < x[1] else 0,
        "n_params": 2,
        "n_values": 4
    },
    8: {
        "execute": lambda x: 1 if x[0] == x[1] else 0,
        "n_params": 2,
        "n_values": 4
    },
    9: {
        "execute": self.change_relative_base,
        "n_params": 1,
        "n_values": 2
    },
    99: {
        "execute": lambda: exit(),
        "n_values": 1
    }
}

    def output(self, value):
        # print(">output>", value)
        self.outputs += value


    def change_relative_base(self, value):
        # print(">>>", value, self.relative_base)
        self.relative_base += value[0]
        # print("<<<", self.relative_base)

    def input(self, _):
        assert len(self.inputs) > 0, "Not enough inputs"
        return self.inputs.pop(0)

    def jump_if_true(self, values):
        if values[0] > 0:
            self.jmp = values[1]

    def jump_if_false(self, values):
        if values[0] == 0:
            self.jmp = values[1]




    def split_instruction(self, instruction):
        opcode = instruction % 100
        parameter_modes = [int(x) for x in reversed(str(instruction // 100))]

        return opcode, parameter_modes + [0, 0] # add some extra zeros for undefined params

    def read_mem(self, address):
        if address >= len(self.memory):
            if address in self.extra_memory:
                return self.extra_memory[address]
            else:
                return 0
        else:
            return self.memory[address]

    def write_mem(self, address, value):
        if address >= len(self.memory):
            self.extra_memory[address] = value
        else:
            self.memory[address] = value

    def read_param(self, param, mode):
        # print(param, mode)
        if mode == 0:
            return self.read_mem(param)
        if mode == 1:
            return param
        if mode == 2:
            return self.read_mem(param + self.relative_base)
        assert True, "Not implemented"

    def write_param(self, param, mode, value):
        if mode == 2:
            self.write_mem(param + self.relative_base, value)
        else:
            self.write_mem(param, value)

    def run(self):

        opcode, parameter_modes = self.split_instruction(self.memory[self.instruction_pointer]) # instruction
        # print(parameter_modes)

        while opcode < 99:
            # print("]", self.instruction_pointer)
            # print(">>", opcode)
            self.jmp = None
            instruction = self.instructions[opcode]

            params = []
            for i in range(instruction["n_params"]):
                params.append(self.read_param(self.memory[self.instruction_pointer + 1 + i], parameter_modes[i]))

            try:
                result = instruction["execute"](params)
            except:
                return 1

            # print("result", result)

            if instruction["n_values"] > (instruction["n_params"] + 1):
                self.write_param(self.memory[self.instruction_pointer + 1 + instruction["n_params"]],
                                 parameter_modes[instruction["n_params"]], result)

            if self.jmp is None:
                self.instruction_pointer += instruction["n_values"] # the number of values in the instruction
            else:
                self.instruction_pointer = self.jmp

            # print("MEM", self.memory)
            if self.halt_on_output and len(self.outputs) > 0: # halt after updating instruction pointer, to let this act as a pause
                return 2

            opcode, parameter_modes = self.split_instruction(self.memory[self.instruction_pointer]) # instruction
        return 0




mem = [int(x) for x in lines[0].rstrip().split(",")]

computer = Intcode(mem, [], False)

status = computer.run()

outputs = computer.outputs

j = 0
i = 0

scaffolds = set()

for c in outputs:
    if c == 10:
        print()
        j = 0
        i += 1
        continue
    else:
        print(chr(c), end="")

        if chr(c) == "#":
            scaffolds.add((i, j))
    j += 1

print(scaffolds)

# exit()

intersections = set()

for scaffold in scaffolds:
    # print(scaffold)
    is_intersection = True
    for direction in DIRECTIONS:
        pos, _ = next_pos(scaffold, direction)
        if pos not in scaffolds:
            is_intersection = False
    if is_intersection:
        intersections.add(scaffold)

print(intersections)

total = 0
for intersection in intersections:
    (i, j) = intersection
    total += (i * j)

print("Part 1", total, "Intersections #", len(intersections))

# address 0 from 1 to 2
# A,B,C (call functions) - max 20 chars
# L,R,1 (define functions) - max 20 chars (3x)
# y | n (video)

mem = [int(x) for x in lines[0].rstrip().split(",")]
mem[0] = 2

# pencil and paper solution:
commands = """A,C,C,A,B,A,B,A,B,C
R,6,R,6,R,8,L,10,L,4
L,4,L,12,R,6,L,10
R,6,L,10,R,8
y
"""



inputs = [ord(x) for x in list(commands)]

computer = Intcode(mem, inputs, False)

status = computer.run()

outputs = computer.outputs

# print(outputs)


for c in outputs:
    if c == 10:
        print()
        j = 0
        i += 1
        continue
    else:
        print(chr(c), end="")

        if chr(c) == "#":
            scaffolds.add((i, j))
    j += 1







