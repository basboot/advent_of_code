from functools import cache
from functools import cache
from itertools import product

from sympy import Symbol, Piecewise, Eq

file1 = open('q24a.txt', 'r')
file_lines = file1.readlines()

# block:
# 00 inp w
# 01 mul x 0
# 02 add x z
# 03 mod x 26
# 04 div z 1 <= block selector, 1 or 26
# 05 add x 12 <= param 1, only relevant for block type 26 (always > 9 for type 1)
# 06 eql x w
# 07 eql x 0
# 08 mul y 0
# 09 add y 25
# 10 mul y x
# 11 add y 1
# 12 mul z y
# 13 mul y 0
# 14 add y w
# 15 add y 7 <= param 2
# 16 mul y x
# 17 add z y


blocks = []
for i in range(0, len(file_lines), 18):
    _, _, selector = file_lines[i + 4].rstrip().split(" ")
    _, _, param1 = file_lines[i + 5].rstrip().split(" ")
    _, _, param2 = file_lines[i + 15].rstrip().split(" ")

    print(selector, param1, param2)

    blocks.append((int(selector), int(param1), int(param2)))

print(blocks)

@cache
# block with div z 1
def block1(z, w, param1, param2):
    assert param1 > 9, "This only works if param1 > 9"

    return 26 * z + w + param2 # Z wordt groter

@cache
# div z 26
def block26(z, w, param1, param2):
    if z % 26 + param1 == w:
        return z // 26 # Z wordt kleiner, en kan 0 worden
    else:
        return 26 * (z // 26) + w + param2 # Z wordt iets kleiner als z % 26 > w + param2, maar geen 0 (w en param2 altijd > 0)


DIGITS = [9, 8, 7, 6, 5, 4, 3, 2, 1]
# DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

@cache
def dfs(z, level):
    # print(level)
    if level == 14:
        if z == 0:
            return True, []
        else:
            return False, []


    for w in DIGITS:
        selector, param1, param2 = blocks[level]

        if selector == 1:
            succes, solution = dfs(block1(z, w, param1, param2), level + 1)
        else:
            # TODO: add other case
            if z % 26 + param1 == w: # or (z % 26 > w + param2 and level < 13): # 97919997299495
                succes, solution = dfs(block26(z, w, param1, param2), level + 1)
            else:
                # toch even proberen
                #succes, solution = dfs(block26(z, w, param1, param2), level + 1)
                continue


        if succes:
            return succes, [w] + solution

    return False, []

print("DFS")
print(dfs(0, 0))


exit()
def get_value(name):
    if name.strip('-').isnumeric():
        return int(name)
    else:
        if name in stored_values:
            return stored_values[name]
        else:
            return 0

def get_input():
    global input
    return input.pop(0)

def execute_instruction(instruction):
    global stored_values

    match instruction[0]:
        case "inp":
            stored_values[instruction[1]] = get_input()
        case "add":
            stored_values[instruction[1]] = get_value(instruction[1]) + get_value(instruction[2])
        case "mul":
            stored_values[instruction[1]] = get_value(instruction[1]) * get_value(instruction[2])
        case "div":
            stored_values[instruction[1]] = get_value(instruction[1]) // get_value(instruction[2])
        case "mod":
            stored_values[instruction[1]] = get_value(instruction[1]) % get_value(instruction[2])
        case "eql":
            #stored_values[instruction[1]] = 1 if get_value(instruction[1]) == get_value(instruction[2]) else 0

            stored_values[instruction[1]] = Piecewise((1, Eq(get_value(instruction[1]), get_value(instruction[2]))), (0, True))
        case _:
            assert True, "unkonwn instruction"


model_number = 0


# print(model_number)
input = ([Symbol(f"x{i}") for i in range(14)])
stored_values = {"z" : Symbol("z")}
# print(program)

expressions = []

first = True
for instruction in program:
    if instruction[0] == "inp":
        if not first:
            expr = stored_values['z']
            print(expr)
            expressions.append(expr)

            input = ([Symbol(f"x{i}") for i in range(14)])
            stored_values = {"z" : Symbol("z")}
        else:
            first = False

    execute_instruction(instruction)


expr = stored_values['z']
expressions.append(expr)

print("-------")

print(expr)

@cache
def get_options_for_output(level, output):
    # print(expressions[level])
    solutions = set()
    # TODO: assume 26 is enough, and only integer values
    for i in range(-1000, 1000):
        for digit in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            solution = expressions[level].subs('x0', digit).subs('z', i)
            if solution == output:
                # print(i, digit)
                solutions.add((i, digit))
    return solutions

@cache
def get_output_options(level, prev_output):
    # print(expressions[level])
    solutions = []

    for digit in [9, 8, 7, 6, 5, 4, 3, 2, 1]:
        solutions.append((expressions[level].subs('x0', digit).subs('z', prev_output), digit))

    return solutions

print(get_output_options(0, 0))


def dfs(state, level, solution_so_far):
    # print(level)
    if level == 14:
        if state == 0:
            print("FOUND", solution_so_far)
            exit()
        else:
            return


    for next_state, next_digit in get_output_options(level, state):
        solution = list(solution_so_far)
        solution.append(next_digit)
        dfs(next_state, level + 1, tuple(solution))


dfs(0, 0, ())

exit()

@cache
def dfs(state, level, solution_so_far):
    print(level)
    if level == -1:
        print("FOUND", solution_so_far)

    for next_state, next_digit in get_options_for_output(level, state):
        solution = list(solution_so_far)
        solution.append(next_digit)
        dfs(next_state, level - 1, tuple(solution))

dfs(0, 13, ())





exit()

first_x = 10
for x in product([9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9], [1, 2, 3, 4, 5, 6 ,7 ,8, 9]):
    # TODO: misschien nog verkeerd om ook?

    # z = x[13] + 26*math.floor(x[12]/26 + math.floor(x[11]/26 + math.floor(x[10]/26 + math.floor(x[9]/26 + math.floor(x[8]/26 + math.floor(x[7] + 26*math.floor(x[6]/26 + math.floor(x[5] + 26*math.floor(x[4] + 26*math.floor(x[3]/26 + math.floor(x[2] + 26*math.floor(x[1] + 26*math.floor(x[0]))) + 128503/26))) + 2191/13)) + 353/26) + 5/13) + 3/13) + 5/13) + 4/13) + 5

    #z = 308915776*x[0] + 11881376*x[1] + x[10] + x[11] + x[12] + x[13] + 456976*x[2] + 17576*x[3] + 17576*x[4] + 676*x[5] + 26*x[6] + 26*x[7] + x[8] + x[9] + 2258683052

    if x[0] < first_x:
        first_x = x[0]
        print(x)

    if z == 0:
        print(x)

# TODO: 14 syms gebruiken, en daarmee zoeken

# zonder integer div
# 308915776*x0 + 11881376*x1 + x10 + x11 + x12 + x13 + 456976*x2 + 17576*x3 + 17576*x4 + 676*x5 + 26*x6 + 26*x7 + x8 + x9 + 2258683052