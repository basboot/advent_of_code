import numpy as np

file1 = open('q6a.txt', 'r')
lines = file1.readlines()

lights = np.zeros((1000, 1000))

for line in lines:
    parts = line.rstrip().split(" ")
    action, start, end = parts[-4], [int(x) for x in parts[-3].split(",")], [int(x) for x in parts[-1].split(",")]

    match action:
        case "on":
            lights[start[0]: end[0] + 1, start[1]: end[1] + 1] += 1
        case "off":
            lights[start[0]: end[0] + 1, start[1]: end[1] + 1] -= 1
        case "toggle":
            lights[start[0]: end[0] + 1, start[1]: end[1] + 1] += 2

    lights[lights < 0] = 0

print(np.sum(lights))

# 14190930 too low