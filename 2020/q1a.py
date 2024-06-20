file1 = open('q1a.txt', 'r')
lines = file1.readlines()

numbers = []
for line in lines:
    numbers.append(int(line.rstrip()))

numbers.sort()
print(numbers)

for i in range(len(numbers)):
    for j in range(len(numbers) - 1, -1, -1):
        if j <= i: # do not cross
            break
        numbers_sum = numbers[i] + numbers[j]

        if numbers_sum == 2020:
            print("FOUND")
            print(numbers[i], "*", numbers[j], "=", numbers[i] * numbers[j])

        if numbers_sum < 2020: # not possible anymore
            break