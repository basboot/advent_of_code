file1 = open('q2a.txt', 'r')
lines = file1.readlines()

numbers = []

total_valid = 0
for line in lines:
    policy, char, password = line.rstrip().replace(":", "").split(" ")
    minimum, maximum = [int(x) for x in policy.split("-")]
    print(minimum, maximum)

    char_count = {}
    for c in password:
        if c in char_count:
            char_count[c] += 1
        else:
            char_count[c] = 1

    if char not in char_count:
        char_count[char] = 0

    print(char_count)

    if char_count[char] >= minimum and char_count[char] <= maximum: # valid
        total_valid += 1


print("Part 1", total_valid)



