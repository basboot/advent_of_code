import math
from collections import Counter
import numpy as np

file1 = open('q8a.txt', 'r')

steps = {}

data = [int(x) for x in file1.readlines()[0].rstrip().split(" ")]

def get_node(data):
    global total
    n_children, n_metadata, *data = data

    child_values = {}
    for i in range(n_children):
        child_value, data = get_node(data)
        child_values[i + 1] = child_value

    metadata = data[:n_metadata]

    value = 0
    if n_children == 0:
        value += sum(metadata)
    else:
        for i in metadata:
            if i in child_values:
                value += child_values[i]

    print(value)
    return value, data[n_metadata:]

print(get_node(data))

