file1 = open('q2a.txt', 'r')
lines = file1.readlines()

keypad = {
    (0, -1): 2,
    (-1, -1): 1,
    (1, -1): 3,
    (0, 0): 5,
    (-1, 0): 4,
    (1, 0): 6,
    (0, 1): 8,
    (-1, 1): 7,
    (1, 1): 9
}

keypad2 = {
    (0, 0): 5,

    (1, -1): 2,
    (1, 0): 6,
    (1, 1): "A",

    (2, -2): 1,
    (2, -1): 3,
    (2, 0): 7,
    (2, 1): "B",
    (2, 2): "D",

    (3, -1): 4,
    (3, 0): 8,
    (3, 1): "C",

    (4, 0): 9,
}

directions = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0)
}

def type_code(position, keypad):
    code = []

    for line in lines:
        moves = list(line.rstrip())

        for move in moves:
            dx, dy = directions[move]
            x, y = position
            new_position = x + dx, y + dy
            # print(position, move, directions[move], new_position)
            if new_position in keypad:
                position = new_position

        code.append(str(keypad[position]))
    return "".join(code)

print("Part 1", type_code((0,0), keypad))

print("Part 2", type_code((0,0), keypad2))

