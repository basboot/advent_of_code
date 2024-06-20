import math
from itertools import permutations

import numpy as np

file1 = open('q21a.txt', 'r')
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

# jump is D is ground, but only if B or C is not ground
# always jump if A is not ground
program_part1 = """NOT D T
NOT T J
NOT B T
NOT T T
AND C T
NOT T T
AND T J
NOT A T
OR T J
WALK
"""

program = """
NOT B J 
NOT C T
OR T J
AND D J; if d is ground and there's a hole at B or C, we can jump to D
AND H J; but only if H is also ground
NOT A T; if next tile is a hole we have to jump
OR T J 
RUN
"""

inputs = []
for line in program.split("\n"):
    if line == "":
        continue
    for c in list(line):
        if c == ";":
            break
        else:
            inputs.append(ord(c))
    inputs.append(10)

computer.inputs = inputs # [ord(x) for x in list(program)]


status = computer.run()

for o in computer.outputs:
    if o < 256:
        print(chr(o), end="")
    else:
        print("Damage", o)

print(computer.outputs)

# springdroid *
# registers J(ump) T(emp)
# sensors *ABCD, part 2:EFGHI
# AND/OR/NOT a b, proces a (and possibly b), store result in b
# 10 = newline
# WALK starts program