from collections import deque

file1 = open('q21a.txt', 'r')

password = deque(list("fbgdceah"))

def swap_positions(password, from_pos, to_pos):
    password[from_pos], password[to_pos] = password[to_pos], password[from_pos]
    return password

# reverse order
lines = file1.readlines()
lines.reverse()

print("".join(password))

for line in lines:
    instruction = line.rstrip().split(" ")
    print(instruction)

    match instruction[0]:
        case "swap": # stays the same
            if instruction[1] == "position":
                password = swap_positions(password, int(instruction[2]), int(instruction[5]))
            else:
                password = swap_positions(password, password.index(instruction[2]), password.index(instruction[5]))
            pass
        case "reverse": # stays the same
            password = deque(list(password)[:int(instruction[2])] + list(password)[int(instruction[2]):int(instruction[4]) + 1][::-1] + list(password)[int(instruction[4]) + 1:])
        case "rotate":
            if instruction[1] == "based":
                # easiest probably just trial and error
                backup_password = tuple(password)
                print("backup", backup_password)

                # try all lengths + 1
                for i in range(len(password) + 1):
                    # reverse rotate
                    test_password = deque(backup_password)
                    test_password.rotate(-i)
                    # perform rotate
                    index_to_rotate = list(test_password).index(instruction[6])
                    # print(index_to_rotate)
                    rotations = 1 + index_to_rotate + (1 if index_to_rotate >= 4 else 0)
                    # print(rotations)
                    test_password.rotate(rotations)
                    if tuple(test_password) == backup_password:
                        # print("FOUND")
                        password.rotate(-i)
                        break
            else: # jusr reverse left and right
                password.rotate(int(instruction[2]) * (1 if instruction[1] == "left" else -1))
        case "move": # reverse from and to
            password = list(password)
            char_to_move = password.pop(int(instruction[5]))
            password.insert(int(instruction[2]), char_to_move)
            password = deque(password)

    print("".join(password))


# rotate based on position of letter b
# rotate based on position of letter d