class Computer():
    def __init__(self, program: list):
        self.program_counter = 0
        self.program = program.copy()
        self.memory = {'a': 0, 'b': 0 }

    def save(self, register, value):
        if register is not None:
            self.memory[register] = value if value > 0 else 0

    def load(self, register):
        return self.memory[register] if register is not None else None

    def execute_instruction(self):
        operation, register, offset = self.program[self.program_counter]
        value = self.load(register)

        # execute
        match (operation):
            case 'hlf':
                value //= 2
            case 'tpl':
                value *= 3
            case 'inc':
                value += 1
            case 'jmp':
                self.program_counter += offset - 1 # -1 to compensate for normal inc
            case 'jie':
                if value % 2 == 0:
                    self.program_counter += offset - 1  # -1 to compensate for normal inc
            case 'jio':
                if value == 1:
                    self.program_counter += offset - 1  # -1 to compensate for normal inc

            case _:
                # memory dump
                assert True, "Unknown instruction: " + operation

        self.program_counter += 1
        self.save(register, value)

    def run(self):
        while self.program_counter < len(self.program):
            self.execute_instruction()

        print("exit normal")
        print(self.memory)

file1 = open('q23a.txt', 'r')
lines = file1.readlines()

program = []


for line in lines:
    operations = line.rstrip().split(", ")

    offset = 0
    if len(operations) == 2:
        offset = int(operations[1])

    operation, register = operations[0].split(" ")

    if operation == 'jmp':
        offset = int(register)
        register = None

    program.append((operation, register, offset))


print(program)

computer = Computer(program)
# Part 2
computer.memory['a'] = 1

computer.run()

