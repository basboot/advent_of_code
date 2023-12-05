# Using readlines()
file1 = open('q4b.txt', 'r')
lines = file1.readlines()


def create_set(sections):
    section = sections.split('-')
    # print(section)
    return set(range(int(section[0]), int(section[1]) + 1))

total = 0

for line in lines:
    elf1, elf2 = line.strip().split(",")
    sections1 = list(create_set(elf1))
    sections2 = list(create_set(elf2))

    for section in sections1:
        if section in sections2:
            total += 1
            break






print(total)

