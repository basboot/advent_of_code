# Using readlines()
file1 = open('q3b.txt', 'r')
lines = file1.readlines()


def get_priority(c):
    return ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27

total = 0
elf = 0
for line in lines:
    elf += 1
    backpack = line.strip()

    if elf == 1:
        comp1 = backpack
        continue
    if elf == 2:
        comp2 = set(backpack)
        continue
    if elf == 3:
        comp3 = set(backpack)

    elf = 0

    for item in comp1:
        if item in comp2 and item in comp3:
            # print(item)
            # print(get_priority(item))
            total += get_priority(item)
            break
    # print(comp1)
    # print(comp2)

print(total)

