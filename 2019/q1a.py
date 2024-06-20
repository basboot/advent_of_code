file1 = open('q1a.txt', 'r')
lines = file1.readlines()

def calc_fuel(weight):
    fuel = weight // 3 - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + calc_fuel(fuel)

total = 0
for line in lines:
    total += calc_fuel(int(line.rstrip()))

print("Part 1", total)

# 5243999 too low

