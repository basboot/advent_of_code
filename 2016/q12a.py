from collections import defaultdict

file1 = open('q12a.txt', 'r')

program = []

for line in file1.readlines():
    data = line.rstrip().split(" ")
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

        self.registers["c"] = c


    def value(self, n):
        try:
            return int(n)
        except:
            return self.registers[n]


    def jump_not_zero(self, n, offset):
        if n != 0:
            return offset - 1 # -1, because counter will always be incremented by one
        else:
            return 0

    def run(self):
        while True:

            if self.program_counter >= len(self.program):
                return 0

            command, parameters = self.program[self.program_counter]

            # print(self.id, self.program_counter, command, parameters, self.registers)

            match command:
                case "cpy":
                    self.registers[parameters[1]] = self.value(parameters[0])
                case "inc":
                    self.registers[parameters[0]] += 1
                case "dec":
                    self.registers[parameters[0]] -= 1
                case "jnz":
                    self.program_counter += self.jump_not_zero(self.value(parameters[0]), self.value(parameters[1]))

            self.program_counter += 1


password_check = Assembunny(0)

print(password_check.run())

print("Part 1", password_check.registers["a"])

password_check2 = Assembunny(1)

# print(password_check2.run())
#
# print("Part 2", password_check2.registers["a"])






