import functools

from bitstring import BitArray

file1 = open('q3a.txt', 'r')
lines = file1.readlines()

import numpy as np

result = None


rows = []
for row in lines:
    # np_row = np.array([int(x) for x in row.rstrip()])
    # if result is None:
    #     result = np_row
    # else:
    #     result = result + np_row
    rows.append([int(x) for x in row.rstrip()])

# gamma = (BitArray(bin="".join([str(int(x)) for x in list(np.round(result / len(lines)))]))).uint
# epsilon = (BitArray(bin="".join([str((1 - int(x))) for x in list(np.round(result / len(lines)))]))).uint

# print(gamma * epsilon)


print(rows)

LEAST_COMMON, MOST_COMMON = 0, 1

def find_matching(values, bit, criterium):
    if len(values) == 1:
        return values[0]

    assert len(values) > 1, "No values matching :-("

    sum_value = 0
    for val in values:
        sum_value += val[bit]


    most_common = round(sum_value / len(values))

    desired = criterium

    print(sum_value / len(values))
    if sum_value / len(values) != 0.5:
        desired = most_common if criterium == MOST_COMMON else abs(most_common - 1)

    new_values = []
    for val in values:
        if val[bit] == desired:
            new_values.append(val)

    print(new_values)

    return find_matching(new_values, bit + 1, criterium)

print()

print(find_matching(rows, 0, MOST_COMMON))

ox = (BitArray(bin="".join([str(x) for x in find_matching(rows, 0, MOST_COMMON)])).uint)
co2 = (BitArray(bin="".join([str(x) for x in find_matching(rows, 0, LEAST_COMMON)])).uint)

print(ox * co2)

