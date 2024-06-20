file1 = open('q5a.txt', 'r')
lines = file1.readlines()

def output(value):
    print("diag", value)

def input(_):
    return 5

jmp = None

def jump_if_true(values):
    global jmp
    if values[0] > 0:
        jmp = values[1]

def jump_if_false(values):
    global jmp
    if values[0] == 0:
        jmp = values[1]

instructions = {
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
        "execute": input,
        "n_params": 0,
        "n_values": 2
    },
    4: {
        "execute": output,
        "n_params": 1,
        "n_values": 2
    },
    5: {
        "execute": jump_if_true,
        "n_params": 2,
        "n_values": 3
    },
    6: {
        "execute": jump_if_false,
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


memory = [int(x) for x in lines[0].rstrip().split(",")]

print(memory)

def split_instruction(instruction):
    opcode = instruction % 100
    parameter_modes = [int(x) for x in reversed(str(instruction // 100))]

    return opcode, parameter_modes + [0, 0] # add some extra zeros for undefined params




def read_param(param, mode):
    # print(param, mode)
    if mode == 0:
        return memory[param]
    if mode == 1:
        return param
    assert True, "Not implemented"


def write_param(param, value):
    # never in immediate
    memory[param] = value

instruction_pointer = 0

opcode, parameter_modes = split_instruction(memory[instruction_pointer]) # instruction
# print(parameter_modes)

while opcode < 99:
    # print(">>", opcode)
    jmp = None
    instruction = instructions[opcode]

    params = []
    for i in range(instruction["n_params"]):
        params.append(read_param(memory[instruction_pointer + 1 + i], parameter_modes[i]))

    result = instruction["execute"](params)

    if instruction["n_values"] > (instruction["n_params"] + 1):
        write_param(memory[instruction_pointer + 1 + instruction["n_params"]], result)

    if jmp is None:
        instruction_pointer += instruction["n_values"] # the number of values in the instruction
    else:
        instruction_pointer = jmp

    opcode, parameter_modes = split_instruction(memory[instruction_pointer]) # instruction

print(memory)
# What value is left at position 0 after the program halts?
print("Part 1", memory[0])

# 7594646
