import math

file1 = open('q1b.txt', 'r')
lines = file1.readlines()

# add zero the align indexes and value
written_numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

total = 0
for line in lines:
    row = line.strip()

    # store both value and position of number
    last_number = [-1, None]
    first_number = [math.inf, None]

    for i in range(len(row)):
        c = row[i]
        if c.isnumeric():
            # same as q1a
            if first_number[1] is None:
                first_number = [i, int(c)]
            last_number = [i, int(c)]

    # possibly update with real numbers
    for i in range(len(written_numbers)):
        index_l = row.find(written_numbers[i])
        index_r = row.rfind(written_numbers[i])

        # update only when a written number has been found
        if index_l > -1:
            if index_l < first_number[0]:
                first_number = [index_l, i]
            if index_r > last_number[0]:
                last_number = [index_r, i]

    total += int(str(first_number[1]) + str(last_number[1]))
    # print(f"line {int(str(first_number[1]) + str(last_number[1]))}, total {total}")

print(total)
