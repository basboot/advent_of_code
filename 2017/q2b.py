file1 = open('q2a.txt', 'r')
lines = file1.readlines()

total = 0
for line in lines:
    numbers = [int(x) for x in line.rstrip().split()]

    for n1 in numbers:
        for n2 in numbers:
            if n1 == n2:
                continue
            if n1 // n2 > 0 and n1 // n2 == n1 / n2:
                total += n1 // n2

print("Part 2", total)
