file1 = open('q14a.txt', 'r')
lines = file1.readlines()

racers = []

DISTANCE, SPEED, DURATION, REST, T, POINTS, NAME = 0, 1, 2, 3, 4, 5, 6

for line in lines:
    name, _, _, speed, _, _, duration, _, _, _, _, _, _, rest, _ = line.rstrip().split(" ")

    print(name, speed, duration, rest)

    racers.append([
        0, # distance
        int(speed),
        int(duration),
        int(rest),
        0, # time in cycle, can only fly when >= 0
        0, # points
        name
    ])

for t in range(2503):
    for i in range(len(racers)):
        if racers[i][T] < 0:
            pass # not flying
        else:
            racers[i][DISTANCE] += racers[i][SPEED]

        racers[i][T] += 1
        if racers[i][T] == racers[i][DURATION]:
            racers[i][T] = -racers[i][REST]

    racers.sort(reverse=True)

    max_dist = racers[0][DISTANCE]

    for i in range(len(racers)):
        if racers[i][DISTANCE] == max_dist:
            racers[i][POINTS] += 1
        else:
            break # sorted so we wont find another

racers.sort(reverse=True, key=lambda x: x[POINTS])

print(racers)

print(f"Part 2: {racers[0][NAME]} wins with points {racers[0][POINTS]}")

# 520 too low