import math
from itertools import permutations

import numpy as np
import pygame
from PIL import Image


file1 = open('q13a.txt', 'r')
lines = file1.readlines()


class Intcode:
    def __init__(self, memory, inputs):
        self.jmp = None

        self.memory = memory

        self.instruction_pointer = 0

        self.relative_base = 0

        self.inputs = inputs

        self.outputs = []

        self.display = np.zeros((44, 20, 3), dtype=np.uint8)

        self.extra_memory = {}

        self.ball = 0
        self.paddle = 0

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
        h, w, _ = self.display.shape
        self.border = 50
        self.scaling_factor = 10

        pygame.init()
        self.win = pygame.display.set_mode(((w + (2 * self.border)) * self.scaling_factor, (h + (2 * self.border)) * self.scaling_factor))

        self.screen = pygame.Surface((w + (2 * self.border), h + (2 * self.border)))

        self.clock = pygame.time.Clock()

        # Get a font for rendering the frame number
        self.basicfont = pygame.font.SysFont(None, 32)
        self.first = True

    def output(self, value):
        # print(">output>", value)
        self.outputs += value

        changed = False
        while len(self.outputs) >= 3:
            changed = True
            x = self.outputs.pop(0)
            y = self.outputs.pop(0)
            tile = self.outputs.pop(0)
            # print(x, y, tile)  # x 0-43, y 0-19
            if x < 0:
                print("Score", tile)
                continue  # this is the score X=-1, Y=0
            match tile:
                case 0:  # empty
                    self.display[x, y] = (255, 255, 255)
                case 1:  # wall
                    self.display[x, y] = (0, 0, 0)
                case 2:  # block
                    self.display[x, y] = (0, 0, 255)
                case 3:  # paddle
                    self.display[x, y] = (0, 255, 0)
                    self.paddle = x
                    # print("Paddle", x)
                case 4:  # ball
                    self.display[x, y] = (255, 0, 0)
                    self.ball = x
                    # print("Ball", x)
        if changed:
            # update display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Clear screen to white before drawing
            self.screen.fill((255, 255, 255))

            # Get a numpy array to display from the simulation
            npimage = computer.display

            # Convert to a surface and splat onto screen offset by border width and height
            surface = pygame.surfarray.make_surface(npimage)
            self.screen.blit(surface, (self.border, self.border))

            # Display and update frame counter
            # text = basicfont.render('Frame: ' + str(N), True, (255, 0, 0), (255, 255, 255))
            # screen.blit(text, (border, h + border))

            self.win.blit(pygame.transform.scale(self.screen, self.win.get_rect().size), (0, 0))
            pygame.display.flip()
            # self.clock.tick(60) # TODO...


    def change_relative_base(self, value):
        # print(">>>", value, self.relative_base)
        self.relative_base += value[0]
        # print("<<<", self.relative_base)

    def input(self, _):
        done = False

        # while not done:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             exit()
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_LEFT:
        #                 self.inputs.append(-1)
        #             if event.key == pygame.K_RIGHT:
        #                 self.inputs.append(-1)
        #             if event.key == pygame.K_SPACE:
        #                 done = True
        if self.first:
            self.inputs = [1]
            self.first = False
        else:
            if self.ball > self.paddle:
                self.inputs = [1]
            else:
                if self.ball < self.paddle:
                    self.inputs = [-1]
                else:
                    self.inputs = [0]

        assert len(self.inputs) > 0, "Not enough inputs"
        # TODO: update display
        # TODO: wait for next input
        print(">", self.inputs)
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

            result = instruction["execute"](params)
            # print("result", result)

            if instruction["n_values"] > (instruction["n_params"] + 1):
                self.write_param(self.memory[self.instruction_pointer + 1 + instruction["n_params"]], parameter_modes[instruction["n_params"]], result)

            if self.jmp is None:
                self.instruction_pointer += instruction["n_values"] # the number of values in the instruction
            else:
                self.instruction_pointer = self.jmp

            # print("MEM", self.memory)

            opcode, parameter_modes = self.split_instruction(self.memory[self.instruction_pointer]) # instruction

            # print("REL", self.relative_base)

            # add display logic



mem = [int(x) for x in lines[0].rstrip().split(",")]
print(mem)

# Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.
mem[0] = 2

computer = Intcode(mem, [])
computer.run()
print("Part 1", computer.outputs)

total = 0




# If the joystick is in the neutral position, provide 0.
# If the joystick is tilted to the left, provide -1.
# If the joystick is tilted to the right, provide 1.

# mem = [int(x) for x in lines[0].rstrip().split(",")]
# print(mem)
# computer = Intcode(mem, [2])
# computer.run()
# print("Part 2", computer.outputs)

# 0 is an empty tile. No game object appears in this tile.
# 1 is a wall tile. Walls are indestructible barriers.
# 2 is a block tile. Blocks can be broken by the ball.
# 3 is a horizontal paddle tile. The paddle is indestructible.
# 4 is a ball tile. The ball moves diagonally and bounces off objects.


# 16309