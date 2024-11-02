import math
from collections import Counter
import numpy as np

file1 = open('q8a.txt', 'r')

steps = {}

data = [int(x) for x in file1.readlines()[0].rstrip().split(" ")]

total = 0

def get_node(data):
    global total
    n_children, n_metadata, *data = data

    for _ in range(n_children):
        data = get_node(data)

    metadata = data[:n_metadata]
    total += sum(metadata)

    return data[n_metadata:]

get_node(data)

print(total)
