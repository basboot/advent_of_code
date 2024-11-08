file1 = open('q13a.txt', 'r')
lines = file1.readlines()

import numpy as np

earliest = int(lines[0].rstrip())
raw_ids = lines[1].rstrip().split(",")

ids = []
for id in raw_ids:
    if id == "x":
        continue
    ids.append(int(id))

print(earliest)


ids = np.array(ids)

first_busses = np.ceil(earliest / ids) * ids

first_bus_index = np.argmin(first_busses)

print("Part 1", ids[first_bus_index] * (first_busses[first_bus_index] - earliest))

