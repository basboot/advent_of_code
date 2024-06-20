file1 = open('q2a.txt', 'r')
lines = file1.readlines()

numbers = []

total_valid = 0
for line in lines:
    policy, char, password = line.rstrip().replace(":", "").split(" ")
    minimum, maximum = [int(x) for x in policy.split("-")]

    count = 0
    for i in range(minimum - 1, maximum, (maximum - (minimum))):
        if i > len(password) - 1: # end of password
            break

        print(password[i], end="")

        if password[i] == char:
            count += 1

    print("#", count)
    if count == 1:
        total_valid += 1


print("Part 2", total_valid)

# 324 too low



