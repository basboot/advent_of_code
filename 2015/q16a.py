from collections import defaultdict

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *


evidence = {
"children": 3,
"cats": 7, # >
"samoyeds": 2,
"pomeranians": 3, # <
"akitas": 0,
"vizslas": 0,
"goldfish": 5, # <
"trees": 3, # >
"cars": 2,
"perfumes": 1
}

file1 = open('q16a.txt', 'r')
lines = file1.readlines()
for line in lines:
    # Sue 1: cars: 9, akitas: 3, goldfish: 0
    info = line.rstrip()
    first_space = info.find(" ")
    second_space = info.find(" ", first_space + 1)
    n = int(info[first_space + 1: second_space - 1])

    found = True
    for fact in info[second_space + 1:].split(", "):
        key, value = fact.split(": ")

        match(key):
            # Part 2
            case "pomeranians" | "goldfish":
                if evidence[key] <= int(value):
                    found = False
                    break
            case "cats" | "trees":
                if evidence[key] >= int(value):
                    found = False
                    break
            # Part 1
            case _:
                # print(key, value)
                if evidence[key] != int(value):
                    found = False
                    break
    if found:
        print(f"Thank you Aunt Sue {n}")