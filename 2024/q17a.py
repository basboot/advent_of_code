file1 = open('q17a.txt', 'r')
lines = file1.readlines()


a, b, c = map(int, [lines[0].rstrip().split(" ")[2], lines[1].rstrip().split(" ")[2], lines[2].rstrip().split(" ")[2]])
program = list(map(int, lines[4].split(" ")[1].split(",")))

register = {
    'A': a,
    'B': b,
    'C': c
}


def read_combo(op, reg):
    if 0 <= op <=3:
        return op
    if 4 <= op <= 6:
        return reg[chr(ord('A') - 4 + op)]

    assert False, "Illegal combo op."

def show_combo(op):
    if 0 <= op <=3:
        return op
    if 4 <= op <= 6:
        return chr(ord('A') - 4 + op)

    assert False, "Illegal combo op."

def dv(op, computer):
    return computer.register['A'] // (2**op)

def adv(op, computer):
    computer.register['A'] = dv(op, computer)
    return computer.ic + 2

def bxl(op, computer):
    computer.register['B'] = computer.register['B'] ^ op
    return computer.ic + 2

def bst(op, computer):
    computer.register['B'] = op % 8
    return computer.ic + 2

def jnz(op, computer):
    if computer.register['A'] == 0:
        return computer.ic + 2
    else:
        return op

def bxc(op, computer):
    computer.register['B'] = computer.register['B'] ^ computer.register['C']
    return computer.ic + 2

def out(op, computer):
    computer.output(op % 8)
    return computer.ic + 2

def bdv(op, computer):
    computer.register['B'] = dv(op, computer)
    return computer.ic + 2

def cdv(op, computer):
    computer.register['C'] = dv(op, computer)
    return computer.ic + 2


instructions = {
    0: ('adv', adv, True, "A = A >> ?"), # name, function, combo?
    1: ('bxl', bxl, False, "B = B ^ ?"),
    2: ('bst', bst, True, "B = ? % 8"),
    3: ('jnz', jnz, False, "if A != 0 goto ?"),
    4: ('bxc', bxc, False, "B = B ^ C"), # op unused
    5: ('out', out, True, "output ? % 8"),
    6: ('bdv', bdv, True, "B = A >> ?"),
    7: ('cdv', cdv, True, "C = A >> ?")
}

class Computer:
    def __init__(self, register, program):
        self.register = register
        self.program = program
        self.ic = 0
        self.out = []

    def output(self, value):
        self.out.append(value)

    def run(self):
        while self.ic < len(self.program):
            instruction, operand = self.program[self.ic: self.ic + 2]
            _, func, combo, _ = instructions[instruction]
            value = operand if not combo else read_combo(operand, self.register)
            self.ic = func(value, self)

        print(",".join([str(o) for o in self.out]))

    def list(self):
        print(self.register)
        print(self.program)
        for i in range(0, len(program), 2):
            instruction, operand = self.program[i: i + 2]
            _, _, combo, txt = instructions[instruction]
            value = operand if not combo else show_combo(operand)
            print(f"{i}: {txt.replace('?', str(value))}")

register['A'] = 105734774294938

computer = Computer(register, program)
computer.list()
computer.run()

