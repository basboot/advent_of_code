file1 = open('q1a.txt', 'r')
lines = file1.readlines()

numbers = [int(x) for x in lines[0].rstrip()]

total = 0
for i in range(len(numbers)):
    n = numbers[i]
    next_n = numbers[(i + len(numbers) // 2) % len(numbers)]

    if n == next_n:
        total += n

print("Part 2", total)