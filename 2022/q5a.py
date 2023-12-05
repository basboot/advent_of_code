# Using readlines()
file1 = open('q5a.txt', 'r')
lines = file1.readlines()

read_stacks = True

total = 0

stacks = [[], [], [], [], [], [], [], [], []] # 9 stacks max


for line in lines:
    row = line.rstrip()
    print("input: ", row)

    if read_stacks:
        if row != "" and row[1] == '1':
            continue
        # print("len", len(row))
        for i in range(len(row)):
            # print(row[i])
            if (i - 1) % 4 == 0:
                if row[i] != ' ':
                    # print(">ADD<", row[i], (i+1) // 4)
                    stacks[(i+1) // 4].append(row[i])
        # print(row)
        if row == "":
            # print("switch")
            read_stacks = False
            print(stacks)
    else:
        # print(row)
        pass
        print("before", stacks)
        print(row[5], row[12], row[17])

        arguments = row.split(' ')

        n_boxes = int(arguments[1])
        from_stack = int(arguments[3])  - 1
        to_stack = int(arguments[5]) - 1

        removed_boxes = stacks[from_stack][0:n_boxes]

        stacks[from_stack] = stacks[from_stack][n_boxes:]

        removed_boxes.reverse() # crane swaps
        stacks[to_stack] =  removed_boxes + stacks[to_stack]
        print("after", stacks)

print(stacks)
print(total)

for stack in stacks:
    if len(stack) > 0:
        print(stack[0], end='')

print()
