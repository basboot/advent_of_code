from collections import Counter
import numpy as np

file1 = open('q5a.txt', 'r')
polymer = list(file1.readlines()[0].rstrip())

# print(polymer)

def is_reactive(a, b):
    return (a.lower() == b.lower()) and (a.islower() != b.islower())

def react(polymer, remove=None):
    result_polymer = []
    i = 0
    while i < len(polymer):
        if (remove is not None) and (polymer[i].lower() == remove):
            i += 1
            continue

        if i == len(polymer) - 1:
            result_polymer.append(polymer[i])
        else:
            if is_reactive(polymer[i], polymer[i + 1]):
                # remove
                i += 1
            else:
                # keep
                result_polymer.append(polymer[i])
        i += 1
    return result_polymer


def reaction_result(polymer, remove=None):
    polymer = polymer.copy()
    reacting_polymer = []
    while len(reacting_polymer) != len(polymer):
        reacting_polymer = polymer
        polymer = react(reacting_polymer, remove)

    return polymer


print("Part 1", len(reaction_result(polymer)))

results = []
for i in range(26):
    remove = chr(ord('a') + i)
    print(remove)
    result = reaction_result(polymer, remove)
    results.append((len(result), remove))

results.sort()
print(results)



