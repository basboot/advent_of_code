file1 = open('q8a.txt', 'r')
lines = file1.readlines()


program = []

# create all nodes
for line in lines:
    row = line.rstrip().split(" ")
    instruction, parameter = row[0], int(row[1])

    print(instruction, parameter)

    program.append((instruction, parameter))



flipped_line = set()
finished = False

while not finished:
    finished = True
    flipped = False
    # run
    program_counter = 0
    executed_lines = set()
    accumulator = 0

    while program_counter < len(program):
        if program_counter in executed_lines:
            print("Failed", flipped_line)
            finished = False
            break

        executed_lines.add(program_counter)

        instruction, parameter = program[program_counter]

        if not flipped and program_counter not in flipped_line and instruction in {"jmp", "nop"}:
            print(program_counter)
            instruction = "jmp" if instruction == "nop" else "nop"
            flipped = True
            flipped_line.add(program_counter)

        match instruction:
            case "acc":
                accumulator += parameter
                program_counter += 1
            case "jmp":
                program_counter += parameter
            case "nop":
                program_counter += 1

print("Part 2", accumulator)

# 48328 too high
