# Using readlines()
file1 = open('q8a.txt', 'r')
lines = file1.readlines()

# count steps from start to goal, goal now is the last char of the position
def count_steps(start, goal):
    steps = 0
    position = start
    while position != goal:
        position = map[position][directions[steps % len(directions)]]
        steps += 1

    return steps

# first line has L,R => 0,1 directions to follow on the map
directions = [0 if x == "L" else 1 for x in list(lines[0].rstrip())]

map = {} # location => (left, right) !indexes are 0 and 1
# also skip second line (whitespace)
for i in range(2, len(lines)):
    location, left, right = lines[i].rstrip().replace(" = (", ",").replace(", ", ",").replace(")", "").split(",")
    map[location] = (left, right)

START = "AAA"
GOAL = "ZZZ"

print("Part 1", count_steps(START, GOAL))

