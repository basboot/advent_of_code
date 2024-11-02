file1 = open('q19a.txt', 'r')
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

reg = (1, 0, 0, 0, 0, 0)

program = []

ip_reg = -1 # -1 not used, 0,... reg == ip
for i in range(len(lines)):
    if lines[i][0] == "#":
        ip_reg = int(lines[i].rstrip().split(" ")[1])
        print("Set ip reg:", ip_reg)
        continue # skip processing
    op, a, b, c = lines[i].rstrip().split(" ")
    command = (op, int(a), int(b), int(c))
    program.append(command)

print(program)

executed = [0] * 40

def line3_11(reg):
    x0, x1, x2, x3, x4, x5 = reg

    if x3 % x4 == 0:
        x1 = x3
        x5 = 1
        x2 = 6
    else:
        x1 = x3 + 1
        x5 = 1
        x2 = 11


    return x0, x1, x2, x3, x4, x5



ip = 0
while ip < len(program):
    # set ip in reg
    if ip_reg > -1:
        reg = tuple([ip if i == ip_reg else int(reg[i]) for i in range(len(reg))])

    # print(f"{ip} {' '.join([str(x) for x in program[ip]])} {reg},", end="")

    if ip == 3:
        reg = line3_11(reg)
    else:
        reg = operate(reg, program[ip])

    # print(f" -> {reg}")

    # executed[ip] += 1
    # if (sum(executed) > 10000):
    #     print(executed)
    #     exit()
    #
    # if ip == 11:
    #     print(executed)
    #     exit()

    # set reg in ip
    if ip_reg > -1:
        ip = reg[ip_reg]

    # inc ip (after setting!)
    ip += 1

print("REG:", reg)

# boosdoeners
# 3, 4, 5, 6
# 7, 8, 9, 10