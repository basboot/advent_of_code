from collections import defaultdict

from numpy.core.defchararray import isnumeric

file1 = open('q23a.txt', 'r')

program = []

for line in file1.readlines():
    data = line.rstrip().split(" --")[0].split(" ")
    command = data[0]
    parameters = data[1:]

    program.append((command, parameters))

bus = [[], []]

class Assembunny:

    def __init__(self, c=0):
        self.program = program
        self.registers = defaultdict(int)
        self.sounds = [0]
        self.n_send = 0
        self.program_counter = 0

        self.n_mul = 0

        self.registers["a"] = c


    def value(self, n):
        try:
            return int(n)
        except:
            return self.registers[n]

    def write_reg(self, reg, value):
        if isnumeric(reg):
            print("ignore invalid instruction")
        else:
            self.registers[reg] = value


    def jump_not_zero(self, n, offset):
        if n != 0:
            return offset - 1 # -1, because counter will always be incremented by one
        else:
            return 0

    def toggle(self, offset):
        toggle_counter = self.program_counter + offset

        # If an attempt is made to toggle an instruction outside the program, nothing happens
        if toggle_counter < 0 or toggle_counter > len(self.program) - 1:
            return

        toggle_command, parameters = self.program[toggle_counter]

        # toggle
        if len(parameters) == 1:
            if toggle_command == "inc":
                toggle_command = "dec"
            else:
                toggle_command = "inc"
        else:
            if toggle_command == "jnz":
                toggle_command = "cpy"
            else:
                toggle_command = "jnz"

        # write to mem
        self.program[toggle_counter] = (toggle_command, parameters)

    def run(self):
        while True:

            if self.program_counter >= len(self.program):
                return 0

            # vanaf 5 t/m 10, a = b * d, d = 0, c = 0
            if self.program_counter == 4:
                self.registers['a'] = self.registers['b'] * self.registers['d']
                self.registers['c'] = 0
                self.registers['d'] = 0
                self.program_counter = 9

            command, parameters = self.program[self.program_counter]

            # print(self.id, self.program_counter, command, parameters, self.registers)

            match command:
                case "cpy":
                    self.write_reg(parameters[1], self.value(parameters[0]))
                case "inc":
                    self.write_reg(parameters[0], self.value(parameters[0]) + 1)
                case "dec":
                    self.write_reg(parameters[0], self.value(parameters[0]) - 1)
                case "jnz":
                    self.program_counter += self.jump_not_zero(self.value(parameters[0]), self.value(parameters[1]))
                case "tgl":
                    self.toggle(self.value(parameters[0]))

            self.program_counter += 1


safe = Assembunny(12)

print(safe.run())

print("Part 1", safe.registers)






# 6 7342
# 7 11662
# 8 46942
# 9 369502
# 10 3635422

# 7342, 11662, 46942, 369502, 3635422