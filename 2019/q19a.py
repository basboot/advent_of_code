import math
from itertools import permutations

import numpy as np

file1 = open('q19a.txt', 'r')
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

# two input instructions to request the X and Y position
# stationary (0) or being pulled by something (1)
# 50x50 area



def in_beam(x, y):
    if x < 0 or y < 0:
        return False

    # We need a fresh computer, because it halts the program after altering mem
    computer = Intcode(mem.copy(), [x, y], False)



    computer.outputs = []

    status = computer.run()

    # changes are small... we could try to reset the computer after running instead of making a new
    # print("---")
    # for i in range(len(mem)):
    #     if mem[i] != computer.memory[i]:
    #         print("DIFF", i)



    return computer.outputs[-1] == 1



total = 0
for y in range(50):
    for x in range (50):

        # print([x, y])

        # assert status == 2, "No output :-("

        if in_beam(x, y):
            total += 1
            # print("#", end="")
        # else:
        #     print(".", end="")

    # print()


print("Part 1", total)

# 114

# TODO: no reset + print output

# start bij [48, 71]
# check 100 naar links en omlaag
# zo niet, ga 1 omlaag, en wandel naar rechts zo lang je in de straal zit

current = (48, 71)
x, y = current

while True:
    if in_beam(x - 99, y + 99):
        print("Part 2", (x - 99) * 10000 + y)
        break
    else:
        y = y + 1
        while in_beam(x + 1, y):
            x += 1

# too high 10771728
# too low 107345
