from collections import Counter

file1 = open('q9a.txt', 'r')
lines = file1.readlines()


PREAMBLE = 25

numbers = []

# create all nodes
for line in lines:
    numbers.append(int(line.rstrip()))

print(numbers)

for i in range(PREAMBLE, len(numbers)):
    previous = Counter(numbers[i - PREAMBLE: i])

    number = numbers[i]

    # assert len(previous) == PREAMBLE

    if len(previous) < PREAMBLE:
        print("Problem for", number, len(previous))
        print(previous)



    # print(number, "must be sum of", previous)

    found = False
    for n in previous:
        other = number - n
        if other not in previous:
            pass
        else:
            if other == number and previous[other] < 2:
                pass
            else:
                # print("found")
                found = True

    invalid_number = number

    if not found:
        print("Part 1", invalid_number)
        break



i = 0
n = 1

while True:
    total = sum(numbers[i: i + n])

    if total < invalid_number:
        n += 1
    else:
        if total > invalid_number:
            i += 1
            n = 1 # to be safe
        else:
            # found
            print("Part 2", min(numbers[i: i + n]), max (numbers[i: i + n]), min(numbers[i: i + n]) + max (numbers[i: i + n]))
            exit()
            break
