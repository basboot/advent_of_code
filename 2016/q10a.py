from collections import Counter
from PIL import Image
from collections import defaultdict


import numpy as np

file1 = open('q10a.txt', 'r')
lines = file1.readlines()

bots = defaultdict(list)

rules = {}

outputs = defaultdict(int)


for line in lines:
    words = line.rstrip().split(" ")

    if words[0] == "value":
        bots[int(words[5])].append(int(words[1]))

    if words[0] == "bot":
        rules[int(words[1])] = (words[5], int(words[6]), words[10], int(words[11]))

need_to_process = True

while need_to_process:
    need_to_process = False
    for bot in list(bots.keys()):
        assert len(bots[bot]) < 3, "!!"
        if len(bots[bot]) == 2:
            # process
            need_to_process = True
            bots[bot].sort() # put in right order

            if bots[bot][0] == 17 and bots[bot][1] == 61:
                print("Part 1", bot)

            low_target, low_id, high_target, high_id = rules[bot]

            if low_target == "bot":
                bots[low_id].append(bots[bot][0])
            else:
                outputs[low_id] += bots[bot][0]

            if high_target == "bot":
                bots[high_id].append(bots[bot][1])
            else:
                outputs[high_id] += bots[bot][1]

            # remove given coins
            bots[bot] = []

print("Part 2", outputs[0] * outputs[1] * outputs[2])
