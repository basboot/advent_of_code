file1 = open('q21a.txt', 'r')
lines = file1.readlines()

# operations
ADD = lambda x, y: x + y
MUL = lambda x, y: x * y
AND = lambda x, y: x & y
OR = lambda x, y: x | y
SET = lambda x, y: x
GT = lambda x, y: 1 if x > y else 0
EQ = lambda x, y: 1 if x == y else 0

# ops = inputs (location + mode) + operation
addr = (False, False, ADD) # A, B both NOT immediate
addi = (False, True, ADD) # A not immediate, B immediate
mulr = (False, False, MUL) # A, B both NOT immediate
muli = (False, True, MUL) # A not immediate, B immediate
banr = (False, False, AND) # A, B both NOT immediate
bani = (False, True, AND) # A not immediate, B immediate
borr = (False, False, OR) # A, B both NOT immediate
bori = (False, True, OR) # A not immediate, B immediate
setr = (False, False, SET) # A, NOT immediate, B ignored by SET
seti = (True, True, SET) # A immediate, B ignored by SET
gtir = (True, False, GT) # value a > reg b
gtri = (False, True, GT) # reg a > value b
gtrr = (False, False, GT) # reg a > reg b
eqir = (True, False, EQ) # value a > reg b
eqri = (False, True, EQ) # reg a > value b
eqrr = (False, False, EQ) # reg a > reg b

ops = addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr

def operate(reg_in, command):
    op, a, b, c = command
    reg_out = list(reg_in)

    operation = globals()[op]

    reg_in1_imm, reg_in2_imm, operation = operation

    A = a if reg_in1_imm else reg_in[a]
    B = b if reg_in2_imm else reg_in[b]
    C = operation(A, B)

    reg_out[c] = C

    return tuple(reg_out)

reg = (0, 0, 0, 0, 0, 0)

program = []

ip_reg = -1 # -1 not used, 0,... reg == ip
for i in range(len(lines)):
    if lines[i][0] == "#":
        ip_reg = int(lines[i].rstrip().split(" ")[1])
        print("Set ip reg:", ip_reg)
        continue # skip processing
    op, a, b, c = lines[i].rstrip().split(" --")[0].split(" ")
    command = (op, int(a), int(b), int(c))
    program.append(command)

print(program)

r5 = set()

ip = 0
print("REG:", reg)
while ip < len(program):
    # set ip in reg
    if ip_reg > -1:
        reg = tuple([ip if i == ip_reg else int(reg[i]) for i in range(len(reg))])

    # print(ip, program[ip])
    reg = operate(reg, program[ip])
    # print("REG:", reg)

    # set reg in ip
    if ip_reg > -1:
        ip = reg[ip_reg]

    # inc ip (after setting!)
    ip += 1


    if ip == 6:
        if reg[5] in r5:
            print("Already seen so take previous")

        r5.add(reg[5])
        print("---- ", reg[5])




print("REG:", reg)

