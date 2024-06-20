import sympy
from sympy import solve

file1 = open('q2a.txt', 'r')
lines = file1.readlines()


intcode = [int(x) for x in lines[0].rstrip().split(",")]

print(intcode)

# before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.
noun = sympy.Symbol('noun', integer=True)
verb = sympy.Symbol('verb', integer=True)

print(intcode)

counter = 0

opcode = intcode[counter]

while opcode < 99:
    print(opcode)
    address1 = intcode[counter + 1]
    address2 = intcode[counter + 2]
    address3 = intcode[counter + 3]

    value1 = noun if address1 == 1 else intcode[address1]
    value2 = verb if address2 == 2 else intcode[address2]

    result = (value1 + value2) if opcode == 1 else (value1 * value2)

    intcode[address3] = result

    counter += 4
    opcode = intcode[counter]

print(intcode)

# 576000*noun + verb + 682644
# Find the input noun and verb that cause the program to produce the output 19690720.
equation = intcode[0] - 19690720
# 576000*noun + verb == 19008076
# Each of the two input values will be between 0 and 99, inclusive
print(equation)

noun = 19008076 // 576000
verb = 19008076 % 576000
print(f"noun {noun} verb {verb}")

# What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)

print(f"Part 2 {100 * noun + verb}")
