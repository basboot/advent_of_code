file1 = open('q2a.txt', 'r')
lines = file1.readlines()

total = 0
for line in lines:
    numbers = [int(x) for x in line.rstrip().split()]
    total += max(numbers) - min(numbers)

print("Part 1", total)
