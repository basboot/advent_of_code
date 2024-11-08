file1 = open('q9a.txt', 'r')
lines = file1.readlines()


in_garbage = False
level = 0
ignore_next = False

count = 0
count_garbage = 0

for character in lines[0].rstrip():
    # print(character)

    if ignore_next:
        ignore_next = False
        continue

    if in_garbage:
        if character == ">":
            in_garbage = False
        else:
            count_garbage += 1
        if character == "!":
            ignore_next = True
            count_garbage -= 1
        continue

    # print("check char", character)
    match character:
        case "{":
            level += 1
            count += level
        case "}":
            level -= 1
        case "!":
            ignore_next = True
        case "<":
            in_garbage = True

print("Part 1", count)
print("Part 2", count_garbage)