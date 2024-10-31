from collections import Counter

import numpy as np

import networkx as nx
from collections import defaultdict

file1 = open('q8a.txt', 'r')
lines = file1.readlines()

registers = defaultdict(int)
registers_max = defaultdict(int) # to keep track of the maximum value ever to exist in a register


operations = {
    "inc": lambda x, v: x + v,
    "dec": lambda x, v: x - v
}

conditional_operations = {
    ">": lambda x, v: x > v,
    "<": lambda x, v: x < v,
    "==": lambda x, v: x == v,
    "<=": lambda x, v: x <= v,
    ">=": lambda x, v: x >= v,
    "!=": lambda x, v: x != v,
}



for line in lines:
    reg_to_modify, operation, value, _, conditional_reg, conditional_operation, condition_value = line.rstrip().split(" ")
    value = int(value)
    condition_value = int(condition_value)
    print(reg_to_modify, operation, value, conditional_reg, conditional_operation, condition_value)

    if conditional_operations[conditional_operation](registers[conditional_reg], condition_value):
        registers[reg_to_modify] = operations[operation](registers[reg_to_modify], value)
        registers_max[reg_to_modify] = max(registers[reg_to_modify], registers_max[reg_to_modify])

print("Part 1", max(registers.values()))
print("Part 2", max(registers_max.values()))