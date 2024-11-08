file1 = open('q10a.txt', 'r')
lines = file1.readlines()

joltages = []

# create all nodes
for line in lines:
    joltages.append(int(line.rstrip()))

joltages.sort()

# add output
joltages.append(joltages[-1] + 3)

current = 0
total = 0

one_dif = 0
three_dif = 0

for jolt in joltages:
    difference = (jolt - current)

    match difference:
        case 1:
            one_dif += 1
        case 3:
            three_dif += 1
    assert difference < 4, "Difference > 3"
    total += (jolt - current)
    current = jolt

print("Part 1", one_dif * three_dif)

# backtrack

# add input 0
joltages = [0] + joltages

print(joltages)

paths = [0] * len(joltages)

# start with 1
paths[0] = 1

i = 0
while i < len(paths):
    offset = 1
    while i + offset < len(paths) and joltages[i + offset] < joltages[i] + 4: # max jump of 3
        paths[i + offset] += paths[i]
        offset += 1

    i += 1

print("Part 2", paths[-1])



# 5488 too low