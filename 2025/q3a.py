joltage1, joltage2 = 0, 0

def find_max_joltage(batteries, n):
    battery_joltage = max(batteries[0:len(batteries) - n])
    if n == 0:
        return battery_joltage
    else:
        battery_index = batteries.index(battery_joltage)
        return battery_joltage * 10**n + find_max_joltage(batteries[battery_index + 1:], n - 1)


with open("q3a.txt") as f:
    for line in f:
        batteries = list(map(int, list(line.strip())))

        joltage1 += find_max_joltage(batteries, 1) # zero indexed, so 2 batteries = 1
        joltage2 += find_max_joltage(batteries, 11)  # zero indexed, so 2 batteries = 1

print(f"Part 1: {joltage1}")
print(f"Part 2: {joltage2}")

