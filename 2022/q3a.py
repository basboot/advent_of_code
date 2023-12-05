# Using readlines()
file1 = open('q3a.txt', 'r')
lines = file1.readlines()


def get_priority(c):
    return ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27

total = 0
for line in lines:
    backpack = line.strip()
    comp1, comp2 = backpack[0:len(backpack) // 2], set(backpack[len(backpack) // 2:])

    for item in comp1:
        if item in comp2:
            # print(item)
            # print(get_priority(item))
            total += get_priority(item)
            break
    # print(comp1)
    # print(comp2)

print(total)

