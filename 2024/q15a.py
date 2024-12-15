file1 = open('q15a.txt', 'r')
lines = file1.readlines()

read_maze = True

walls = set()
boxes = set()

robot = 0
instructions = []

for i, line in enumerate(lines):
    row = line.rstrip()
    if row == "":
        read_maze = False
        continue

    if read_maze:
        for j, value in enumerate(list(row)):
            position = i + j * 1j
            match value.upper():
                case "#":
                    walls.add(position)
                case "O":
                    boxes.add(position)
                case "@":
                    robot = position

    else:
        instructions.extend(list(row))

total = 0

DIRECTIONS = {
    "<": -1j,
    "^": -1,
    ">": 1j,
    "v": 1
}

ROBOT, BOX = 0, 1

def show_warehouse(n):
    for i in range(n):
        for j in range(n):
            position = i + 1j*j

            if position in boxes:
                print("O", end="")
            else:
                if position in walls:
                    print("#", end="")
                else:
                    if position == robot:
                        print("@", end="")
                    else:
                        print(".", end="")
        print()

def can_move(position, direction):
    if position + direction in walls:
        return False
    if position + direction in boxes:
        return move(BOX, position + direction, direction)
    return True

def move(object, position, direction):
    global robot
    global boxes
    if can_move(position, direction):
        if object == ROBOT:
            robot = position + direction
        else:
            boxes.remove(position)
            boxes.add(position + direction)
        return True
    return False


for instruction in instructions:
    # show_warehouse(10)
    move(ROBOT, robot, DIRECTIONS[instruction])
# show_warehouse(10)
for box in boxes:
    total += box.imag + 100 * box.real

print(f"Part 1, {total}")


# 1541701 too low