file1 = open('q8a.txt', 'r')
lines = file1.readlines()


program = []

# create all nodes
for line in lines:
    row = line.rstrip().split(" ")
    instruction, parameter = row[0], int(row[1])

    print(instruction, parameter)

    program.append((instruction, parameter))

# run
program_counter = 0
executed_lines = set()
accumulator = 0

while program_counter not in executed_lines:
    executed_lines.add(program_counter)

    instruction, parameter = program[program_counter]

    match instruction:
        case "acc":
            accumulator += parameter
            program_counter += 1
        case "jmp":
            program_counter += parameter
        case "nop":
            program_counter += 1

print("Part 1", accumulator)


