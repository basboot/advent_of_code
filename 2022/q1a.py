# Using readlines()
file1 = open('q1a.txt', 'r')
lines = file1.readlines()

elves = []
calories = 0

for line in lines:
    calory = line.strip()
    if calory == "":
        elves.append(calories)
        calories = 0
    else:
        calories += int(calory)

elves.sort(reverse=True)

for i in range(3):
    print(elves[i])

print(sum(elves[0:3]))