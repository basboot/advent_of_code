import itertools
from collections import defaultdict
from random import random, shuffle

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *
import re


file1 = open('q19a.txt', 'r')
lines = file1.readlines()

replacements = defaultdict(list)

reversed_replacements = defaultdict(str)

medicine = None

for i in range(len(lines)):
    line = lines[i].rstrip()

    if line == "":
        medicine = lines[i + 1].rstrip()
        break

    in_molecule, out_molecule = line.split(" => ")
    replacements[in_molecule].append(out_molecule)
    reversed_replacements[out_molecule] = in_molecule

print(medicine)

print(replacements)

medicines = set()

for in_molecule in replacements.keys():
    print(in_molecule)
    locations = [m.start() for m in re.finditer(in_molecule, medicine)] # (f"(?={in_molecule})", medicine)]

    for location in locations:
        for out_molecule in replacements[in_molecule]:

            new_medicine = medicine[0:location] + out_molecule + medicine[location + len(in_molecule):]
            medicines.add(new_medicine)
            print(location, in_molecule, out_molecule, new_medicine)


print(medicines)
print("Part 1", len(medicines))

print(reversed_replacements)

# random walk
tmp_medicine = medicine
steps = 0

while True:
    r = list(reversed_replacements.keys())
    shuffle(r) # randomness

    r.sort(key=lambda x: len(x), reverse=True) # greedy
    medicine_before = tmp_medicine
    change = False
    for out_molecule in r:

        locations = [m.start() for m in re.finditer(out_molecule, medicine)]
        for location in locations:
            if np.random.random() < 0.5: # random replacement

                tmp_medicine = tmp_medicine[0:location] + reversed_replacements[out_molecule] + tmp_medicine[location + len(out_molecule):]
                steps += 1



                if tmp_medicine == "e":
                    print("Part 2", steps)
                    exit()
                change = True
                break # max one replacement at a time
        # if change:
        #     break

    if steps > 1000: # medicine_before == tmp_medicine or
        print("No change reset", steps, tmp_medicine)
        tmp_medicine = medicine
        steps = 0


# 638 too high


# HOOH (via H => HO on the first H).
# HOHO (via H => HO on the second H).
# OHOH (via H => OH on the first H).
# HOOH (via H => OH on the second H).
# HHHH (via O => HH).