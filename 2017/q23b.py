from collections import defaultdict

import sympy

file1 = open('q23b.txt', 'r')

program = []

for line in file1.readlines():
    if line[0] == "#":
        continue
    data = line.rstrip().split(" ")
    command = data[0]
    parameters = data[1:]

    program.append((command, parameters))

bus = [[], []]

class Coprocessor:

    def __init__(self, id):
        self.program = program
        self.registers = defaultdict(int)
        self.sounds = [0]
        self.n_send = 0
        self.program_counter = 0
        self.counts = [0] * len(self.program)

        self.id = id
        print("Init process", id)

        self.n_mul = 0

        # disable debug
        self.registers["a"] = 1


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

            print(self.program_counter, command, parameters, self.registers)

            self.counts[self.program_counter] += 1

            # if sum(self.counts) > 500000:
            #     print(self.counts)
            #     exit()

            match command:
                case "snd":
                    self.send(self.value(parameters[0]))
                case "set":
                    self.registers[parameters[0]] = self.value(parameters[1])
                case "add":
                    self.registers[parameters[0]] += self.value(parameters[1])
                case "sub":
                    self.registers[parameters[0]] -= self.value(parameters[1])
                case "mul":
                    self.n_mul += 1
                    self.registers[parameters[0]] *= self.value(parameters[1])
                case "mod":
                    self.registers[parameters[0]] %= self.value(parameters[1])
                case "rcv":
                    message = self.receive()
                    if message is not None:
                        self.registers[parameters[0]] = message
                    else:
                        return 1
                case "jgz":
                    self.program_counter += self.jump_greater_than_zero(self.value(parameters[0]), self.value(parameters[1]))
                case "jnz":
                    self.program_counter += self.jump_not_zero(self.value(parameters[0]), self.value(parameters[1]))

            self.program_counter += 1


# coprocessor = Coprocessor(0)
#
# print(coprocessor.run())
#
# print("Part 2", coprocessor.registers["h"])

b = 109300
c = 126300

h = 0
for i in range(b, c + 17, 17):
    if not sympy.isprime(i):
        h += 1

print("Part 2", h)




