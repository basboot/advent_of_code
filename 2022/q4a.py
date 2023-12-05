# Using readlines()
file1 = open('q4a.txt', 'r')
lines = file1.readlines()


def create_set(sections):
    section = sections.split('-')
    # print(section)
    return set(range(int(section[0]), int(section[1]) + 1))

total = 0
for line in lines:
    elf1, elf2 = line.strip().split(",")
    sections1 = create_set(elf1)
    sections2 = create_set(elf2)

    # print(elf1, elf2)
    # print(sections1, sections2)
    if sections1.issubset(sections2) or sections2.issubset(sections1):

        total += 1






print(total)

