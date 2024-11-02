file1 = open('q16a.txt', 'r')
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

ops_map = []
for i in range(16):
    ops_map.append(set(ops))

def operate(reg_in, command, force_op=None):
    op, a, b, c = command
    reg_out = list(reg_in)

    if force_op == None:
        assert len(ops_map[op]) == 1, "no unique op code for" + str(op)
        operation = tuple(list(ops_map[op])[0])
    else:
        operation = force_op

    reg_in1_imm, reg_in2_imm, operation = operation

    A = a if reg_in1_imm else reg_in[a]
    B = b if reg_in2_imm else reg_in[b]
    C = operation(A, B)

    reg_out[c] = C

    return tuple(reg_out)


def number_of_options(before, command, after):
    count = 0
    global ops_map
    for op in ops:
        if operate(before, command, op) == after:
            print(op)
            count += 1
        else:
            if op in ops_map[command[0]]:
                ops_map[command[0]].remove(op)
    return count

before = (3, 2, 1, 1)
command = (9, 2, 1, 2)
after = (3, 2, 2, 1)


print(operate(before, command, mulr))

total_over_three = 0
start_program = 0
for i in range(0, len(lines), 4):
    if lines[i].rstrip().split(":")[0] == "Before":
        start_program = i + 6
        before = tuple([int(x) for x in lines[i].rstrip().split(": ")[1].replace("[", "").replace("]", "").split(", ")])
        command = tuple([int(x) for x in lines[i + 1].rstrip().split(" ")])
        after = tuple([int(x) for x in lines[i + 2].rstrip().replace("  ", " ").split(": ")[1].replace("[", "").replace("]", "").split(", ")])

        if number_of_options(before, command, after) >= 3:
            total_over_three += 1

print("Part 1", total_over_three)
# 466 too low


# part one has removed all illegal options, now use uniqueness of opcodes to sort them out further

change = True

while change:
    print("RUN CLEANUP")
    change = False
    for i in range(len(ops_map)):
        if len(ops_map[i]) == 1: # fixed, so remove from others
            op_to_remove = list(ops_map[i])[0]
            for j in range(len(ops_map)):
                if i == j:
                    continue # skip self
                if op_to_remove in ops_map[j]:
                    ops_map[j].remove(op_to_remove)
                    change = True
                    print("REMOVE")


print(">>", lines[start_program])
for i in range(len(ops_map)):
    print(i, ops_map[i])

# assume reg is empty

reg = (0, 0, 0, 0)

for i in range(start_program, len(lines)):
    command = tuple([int(x) for x in lines[i].rstrip().split(" ")])
    print(command)
    reg = operate(reg, command)
    print("REG:", reg)


# output mapping to use it for day 19
for opcode in range(len(ops_map)):
    instruction = list(ops_map[opcode])[0]
    for i in range(len(ops)):
        if ops[i] == instruction:
            print(f"{i}, ", end="")
print()