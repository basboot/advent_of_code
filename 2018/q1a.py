file1 = open('q1a.txt', 'r')
lines = file1.readlines()

total = 0

for line in lines:
    total += int(line.rstrip())


print("Part 1", total)

freqs = set()

total = 0
i = 0
while True:
    value = int(lines[i].rstrip())
    total += value

    # ending criterium
    if total in freqs:
        print("Part 2", total)
        break
    else:
        freqs.add(total)

    i += 1
    if i == len(lines):
        i = 0






