file1 = open('q16a.txt', 'r')

instructions = [(x[0], int (x[1:]) if x[0] == 's' else [int(y) if x[0] == 'x' else y for y in x[1:].split("/")]) for x in file1.readlines()[0].rstrip().split(",")]

print(instructions)

start = "abcdefghijklmnop"
line = list(start)

i = 0
fastforwarded = False
while i < 1000000000:
    for move, parameters in instructions:
        match move:
            case 's':
                line = line[-parameters:] + line[:-parameters]

            case 'x':
                left, right = parameters
                line[left], line[right] = line[right], line[left]

            case 'p':
                # TODO: make more efficient?
                left, right = line.index(parameters[0]), line.index(parameters[1])
                line[left], line[right] = line[right], line[left]
    i += 1

    endmove = "".join(line)

    if not fastforwarded:
        if endmove == start:
            print(f"Found repetition after {i} moves")

            i = (1000000000 // i) * i

            print(f"fastforward to i = {i}")
            fastforwarded = True

print("Part 2", "".join(line))


