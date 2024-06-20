file1 = open('q2a.txt', 'r')
lines = file1.readlines()


intcode = [int(x) for x in lines[0].rstrip().split(",")]

print(intcode)

# before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.
intcode[1] = 12
intcode[2] = 2

print(intcode)

counter = 0

opcode = intcode[counter]

while opcode < 99:
    print(opcode)
    address1 = intcode[counter + 1]
    address2 = intcode[counter + 2]
    address3 = intcode[counter + 3]

    value1 = intcode[address1]
    value2 = intcode[address2]

    result = (value1 + value2) if opcode == 1 else (value1 * value2)

    intcode[address3] = result

    counter += 4
    opcode = intcode[counter]

print(intcode)

# What value is left at position 0 after the program halts?
print("Part 1", intcode[0])
