from collections import defaultdict

file1 = open('q23a.txt', 'r')

program = []

for line in file1.readlines():
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

        self.id = id
        print("Init process", id)

        self.n_mul = 0


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

            # print(self.id, self.program_counter, command, parameters, self.registers)

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


coprocessor = Coprocessor(0)

print(coprocessor.run())

print("Part 1", coprocessor.n_mul)




