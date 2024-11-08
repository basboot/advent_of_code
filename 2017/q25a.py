from collections import defaultdict

file1 = open('q25a.txt', 'r')

lines = file1.readlines()

state = lines[0].rstrip().split(" ")[3][0]
position = 0

target_steps = int(lines[1].rstrip().split(" ")[5])
# print(state, target_steps)

state_definitions = {}

for i in range(3, len(lines), 10):
    # print(lines[i + 4].rstrip())

    state_def = lines[i].rstrip().split(" ")[2][0]
    write_0 = int(lines[i + 2].rstrip().split(" ")[-1][0])
    move_0 = -1 if lines[i + 3].rstrip().split(" ")[-1] == "left." else 1
    next_state_0 = lines[i + 4].rstrip().split(" ")[-1][0]

    write_1 = int(lines[i + 6].rstrip().split(" ")[-1][0])
    move_1 = -1 if lines[i + 7].rstrip().split(" ")[-1] == "left." else 1
    next_state_1 = lines[i + 8].rstrip().split(" ")[-1][0]

    # print(write_0, move_0, next_state_0)
    # print(write_1, move_1, next_state_1)

    state_definitions[state_def] = [
        (write_0, move_0, next_state_0), #0
        (write_1, move_1, next_state_1) #1
    ]


tape = defaultdict(int) # dict with bit values

for _ in range(target_steps):
    write, move, next_state = state_definitions[state][tape[position]]

    tape[position] = write
    position += move
    state = next_state

print("Part 1", sum(tape.values()))