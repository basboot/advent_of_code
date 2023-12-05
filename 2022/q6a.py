# Using readlines()
file1 = open('q6a.txt', 'r')
lines = file1.readlines()

SEQUENCE_LENGTH = 14

for line in lines:
    row = line.rstrip()

    # use first char as default to avoid finding a start sequence
    sequence = row[0] * SEQUENCE_LENGTH

    for i in range(len(row)):
        c = row[i]
        # print(c)
        sequence = (sequence + c)[1:]

        if len(set(sequence)) == SEQUENCE_LENGTH:
            print(f"found start sequence at position: {i + 1}")
            break
        # print(sequence)



