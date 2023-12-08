# Using readlines()
file1 = open('q8a.txt', 'r')
lines = file1.readlines()

import numpy as np

# count steps from start to goal, goal now is the last char of the position
def count_steps(start, goal, find_n_times=1):
    steps = 0
    position = start
    while find_n_times > 0:
        position = map[position][directions[steps % len(directions)]]
        steps += 1

        if position[2] == goal:
            find_n_times -= 1

    return steps, position

# first line has L,R => 0,1 directions to follow on the map
directions = [0 if x == "L" else 1 for x in list(lines[0].rstrip())]

map = {} # location => (left, right) !indexes are 0 and 1
# also skip second line (whitespace)
for i in range(2, len(lines)):
    location, left, right = lines[i].rstrip().replace(" = (", ",").replace(", ", ",").replace(")", "").split(",")
    map[location] = (left, right)

# find all starting positions, ending with "A"
START = []
# find all start locations
for location in map:
    if location[2] == "A":
        START.append(location)

GOAL = "Z"

solutions = []
multiple = 1
for start in START:
    solution, _, solution2, _ , solution3, _ = count_steps(start, GOAL) + count_steps(start, GOAL, 2) + count_steps(start, GOAL, 3)
    multiple *= solution
    print(f"Find goal from {start} in {solution} steps, next in {solution2 - solution}, next in {solution3 - solution2} steps.")
    solutions.append(solution)

print("Part 2", np.lcm.reduce(solutions))


