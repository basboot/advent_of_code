file1 = open('q8a.txt', 'r')
file_lines = file1.readlines()

# be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
# fdgacbe cefdb cefbgd gcbe
displays = []

def analyze_segments(unique, output):
    numbers = [None] * 10

    unique.sort(reverse=True) # TODO: er gaat iets mis door de volgorde!

    # find easy numbers first, 1, 4, 7, 8
    for number in unique:
        match len(number):
            case 2:
                numbers[1] = set(list(number))
            case 4:
                numbers[4] = set(list(number))
            case 3:
                numbers[7] = set(list(number))
            case 7:
                numbers[8] = set(list(number))
            case _:
                pass

    # find 9, 6 digits, overeenkomst met 4
    for number in unique:
        n = set(list(number))
        if len(n) == 6 and n.intersection(numbers[4]) == numbers[4]:
            numbers[9] = n

    # find 0, 6 digits, overeenkomst met 1
    for number in unique:
        n = set(list(number))
        if len(n) == 6 and n != numbers[9] and n.intersection(numbers[1]) == numbers[1]:
            numbers[0] = n

    # find 6, last 6 digit
    for number in unique:
        n = set(list(number))
        if len(n) == 6 and n != numbers[9] and n != numbers[0]:
            numbers[6] = n

    # 3 is, 5 digits,  overeenkomst met 7
    for number in unique:
        n = set(list(number))
        if len(n) == 5 and n.intersection(numbers[7]) == numbers[7]:
            numbers[3] = n

    # 2, 9 - 8 = e, 5 digits overeenkomst met e
    e = numbers[8] - numbers[9]
    for number in unique:
        n = set(list(number))
        if len(n) == 5 and n.intersection(e) == e:
            numbers[2] = n

    # 5 is, 5 digits die over is
    for number in unique:
        n = set(list(number))
        if len(n) == 5 and n != numbers[3] and n != numbers[2]:
            numbers[5] = n


    # print(numbers)


    result = 0
    for n in output:
        result *= 10
        value = 0
        for i in range(10):
            if numbers[i] == set(list(n)):
                value = i
        result += value

    return result


total = 0
total2 = 0
for i in range(len(file_lines)):
    unique, output = [x.split() for x in file_lines[i].rstrip().split(" | ")]

    # print(unique, output)

    for digit in output:
        if len(digit) in {2, 4, 3, 7}:
            total += 1

    print(analyze_segments(unique, output))
    total2 += analyze_segments(unique, output)

print(total)
print(total2)

# 984719 too high

# 532 too high

# 1, 4, 7, and 8

# 0: 6, 1:2, 2: 5, 3: 5: 4: 4
# 5: 5, 6: 6, 7: 3, 8: 7: 9: 6

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# 7 segmenten
# 0: 6, 1:2, 2: 5, 3: 5: 4: 4
# 5: 5, 6: 6, 7: 3, 8: 7: 9: 6
# 1, 4, 7, 8 gevonden
# a is verschil tussen 7 en 1
# 9 is, 6 digits, overeenkomst met 4
# 0 is, 6 digits, overeenkomst met 1
# 6 is, 6 digits die over is
# 3 is, 5 digits,  overeenkomst met 7
# 2, 9 - 8 = e, 5 digits overeenkomst met e
# 5 is, 5 digits die over is

