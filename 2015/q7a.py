from collections import defaultdict

import numpy as np
from numpy.core.defchararray import isnumeric

file1 = open('q7a.txt', 'r')
lines = file1.readlines()

wires = {}

binary_operations = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y,
}

def get_value(wire: str):
    if isnumeric(wire):
        return int(wire)
    else:
        # if wire == "b": # part 2
        #     return 3176
        return wires[wire] if wire in wires else None



while len(lines) > 0:
    unprocessed = []
    for line in lines:
        input_wires, output_wire = line.rstrip().split(" -> ")

        operations = input_wires.split(" ")

        value = None

        match len(operations):
            case 1: # 123 -> x
                value = get_value(operations[0]) #get_value(operations[0])
            case 2: # NOT x -> h
                value = get_value(operations[1])
                if value is not None:
                    value = get_value(operations[1]) ^ 65535 # invert only last 16 bits
            case 3:
                value1 = get_value(operations[0])
                value2 = get_value(operations[2])
                if value1 is not None and value2 is not None:
                    value = binary_operations[operations[1]](value1, value2)

        if value is None:
            unprocessed.append(line)
        else:
            wires[output_wire] = value
    lines = unprocessed

print(wires)

print("Part 1 wire A", wires["a"])