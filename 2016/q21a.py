from collections import deque

file1 = open('q21a.txt', 'r')

password = deque(list("abcde"))

def swap_positions(password, from_pos, to_pos):
    password[from_pos], password[to_pos] = password[to_pos], password[from_pos]
    return password

for line in file1.readlines():
    instruction = line.rstrip().split(" ")
    print(instruction)

    match instruction[0]:
        case "swap":
            if instruction[1] == "position":
                password = swap_positions(password, int(instruction[2]), int(instruction[5]))
            else:
                password = swap_positions(password, password.index(instruction[2]), password.index(instruction[5]))
            pass
        case "reverse":
            password = deque(list(password)[:int(instruction[2])] + list(password)[int(instruction[2]):int(instruction[4]) + 1][::-1] + list(password)[int(instruction[4]) + 1:])
        case "rotate":
            if instruction[1] == "based":
                print("---")
                index_to_rotate = list(password).index(instruction[6])
                # print(index_to_rotate)
                rotations = 1 + index_to_rotate + (1 if index_to_rotate >= 4 else 0)
                # print(rotations)
                password.rotate(rotations)
            else:
                password.rotate(int(instruction[2]) * (1 if instruction[1] == "right" else -1))
        case "move":
            password = list(password)
            char_to_move = password.pop(int(instruction[2]))
            password.insert(int(instruction[5]), char_to_move)
            password = deque(password)

    print("".join(password))
