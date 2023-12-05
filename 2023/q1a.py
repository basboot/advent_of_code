file1 = open('q1a.txt', 'r')
lines = file1.readlines()

total = 0
for line in lines:
    row = line.strip()

    last_number = None
    first_number = None

    for c in row:
        if c.isnumeric():
            # only set first on first occurence of digit
            if first_number is None:
                first_number = int(c)
            # always set/overwrite second to find last occurence
            last_number = int(c)

    total += int(str(first_number) + str(last_number))

print(total)
