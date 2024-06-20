import math
from itertools import permutations
from PIL import Image

from tools.advent_tools import *

file1 = open('q11a.txt', 'r')
lines = file1.readlines()


class Intcode:
    def __init__(self, memory, inputs):
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

            opcode, parameter_modes = self.split_instruction(self.memory[self.instruction_pointer]) # instruction
        return 0


mem = [int(x) for x in lines[0].rstrip().split(",")]
painting_robot = Intcode(mem, [])

white_tiles = set()
position = (0, 0)
direction = NORTH

def get_color(position):
    if position in white_tiles:
        return 1
    else:
        return 0

painted = set()

done = False
while not done:
    painting_robot.inputs.append(get_color(position))
    status = painting_robot.run()

    if status == 0:
        done = True

    color, turn = painting_robot.outputs # 0 black, 1 white, 0 left 1 right
    painting_robot.outputs = []
    if color == 0 and position in white_tiles:
        white_tiles.remove(position)
        painted.add(position)
    if color == 1 and position not in white_tiles:
        white_tiles.add(position)
        painted.add(position)
    direction = (direction + (-1 if turn == 0 else 1)) % 4
    position, _ = next_pos(position, direction)

print("Part 1", len(painted))


## part 2

mem = [int(x) for x in lines[0].rstrip().split(",")]
painting_robot = Intcode(mem, [])

white_tiles = {(0, 0)}
position = (0, 0)
direction = NORTH

def get_color(position):
    if position in white_tiles:
        return 1
    else:
        return 0

painted = set()

done = False
while not done:
    painting_robot.inputs.append(get_color(position))
    status = painting_robot.run()

    if status == 0:
        done = True

    color, turn = painting_robot.outputs # 0 black, 1 white, 0 left 1 right
    painting_robot.outputs = []
    if color == 0 and position in white_tiles:
        white_tiles.remove(position)
        painted.add(position)
    if color == 1 and position not in white_tiles:
        white_tiles.add(position)
        painted.add(position)
    direction = (direction + (-1 if turn == 0 else 1)) % 4
    position, _ = next_pos(position, direction)

print("Part 2", len(painted))

tiles = list(white_tiles)

xs = []
ys = []
for tile in tiles:
    x, y = tile
    xs.append(x)
    ys.append(y)

print(min(xs), max(xs))
print(min(ys), max(ys))

marking = np.zeros((6, 40))
for tile in tiles:
    i, j = tile
    marking[i, j] = 1

im = Image.fromarray((np.array(marking)).astype('uint8') * 255)
im.show()








