import math

import numpy as np

file1 = open('q7a.txt', 'r')
file_lines = file1.readlines()

crab_list = [int(x) for x in file_lines[0].rstrip().split(",")]

crab_list.sort() # sort

crabs = np.array(crab_list)


# (n * (n+1)) / 2 https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_⋯
last_answer = math.inf
for crab in range(crab_list[0], crab_list[-1] + 1):
    print(crab, "---")

    distances = np.abs(crabs - crab)

    # part 1
    fuel = distances

    fuel = (distances * (distances+1)) / 2

    answer = np.sum(fuel)
    print(answer)

    # too far
    if answer > last_answer:
        answer = last_answer
        break
    last_answer = answer

print("Answer", answer)