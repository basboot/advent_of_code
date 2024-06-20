import math
from itertools import permutations

file1 = open('q7a.txt', 'r')
lines = file1.readlines()


class Intcode:
    def __init__(self, memory, inputs):
        self.jmp = None

        self.memory = memory

        self.instruction_pointer = 0

        self.inputs = inputs

        self.outputs = []

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
    99: {
        "execute": lambda: exit(),
        "n_values": 1
    }
}

    def output(self, value):
        # print(">output>", value)
        self.outputs += value

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




    def read_param(self, param, mode):
        # print(param, mode)
        if mode == 0:
            return self.memory[param]
        if mode == 1:
            return param
        assert True, "Not implemented"


    def write_param(self, param, value):
        # never in immediate
        self.memory[param] = value


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
                self.write_param(self.memory[self.instruction_pointer + 1 + instruction["n_params"]], result)

            if self.jmp is None:
                self.instruction_pointer += instruction["n_values"] # the number of values in the instruction
            else:
                self.instruction_pointer = self.jmp

            # print("MEM", self.memory)

            opcode, parameter_modes = self.split_instruction(self.memory[self.instruction_pointer]) # instruction
        return 0


N_COMPUTERS = 5

max_output = -math.inf
max_settings = None
for settings in permutations([5, 6, 7, 8, 9]):
    computers = []
    for n in range(N_COMPUTERS):
        mem = [int(x) for x in lines[0].rstrip().split(",")]
        computers.append(Intcode(mem, []))
        computers[n].inputs = [settings[n]] # put initial setting in input

    computers[N_COMPUTERS - 1].outputs = [0]

    done = False
    n = 0

    print("START -----")
    while not done:
        for n in range(N_COMPUTERS):
            setting = settings[n]
            computer = computers[n]
            # assert len(computers[n - 1].outputs) == 1, "multiple outputs detected"
            last_output = computers[n - 1].outputs
            # print("*", computers[n - 1].outputs, last_output)
            computers[n - 1].outputs = [] # reset output (consumed bu next computers input)
            computer.inputs += last_output # add last output to input (only needed because inital a setting is in input)
            status = computer.run()
            # print(n, status)
            if status == 0: # normal termination (1 = halt on input)
                done = True
            # print(computer.outputs)

            last_output = computer.outputs[-1]  # double, but needed for last run
            print(n, "OUTPUT", last_output, settings)


    if last_output > max_output:
        max_output = last_output
        max_settings = settings




print(max_output, max_settings)