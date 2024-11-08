from functools import reduce

import networkx as nx


# from day 10
def knot_hash(input):
    lengths = [ord(x) for x in input]
    lengths += [17, 31, 73, 47, 23]

    SIZE = 256

    knot_list = list(range(SIZE))

    position = 0
    skip_size = 0

    length = lengths[0]

    def swap_list(start, length, knot_list):
        for i in range(length // 2):
            temp = knot_list[(start + i) % SIZE]
            knot_list[(start + i) % SIZE] = knot_list[(start + length - i - 1) % SIZE]
            knot_list[(start + length - i - 1) % SIZE] = temp


    for _ in range(64):  # 64x
        for length in lengths:
            swap_list(position, length, knot_list)
            position = (position + length + skip_size) % SIZE
            skip_size += 1

    # now xor

    result = ""
    for i in range(16):
        result += (format(reduce(lambda i, j: int(i) ^ int(j), knot_list[i * 16: (i + 1) * 16]), 'x').zfill(2))

    return result

puzzle = "uugsqrei"

total = 0

disk = set()

for i in range(128):
    integer_value = int(knot_hash(f"{puzzle}-{i}"), 16)
    binary_string = bin(integer_value)[2:] # cut odd 0b
    while len(binary_string) < 128: # add leading zeros to align bits
        binary_string = "0" + binary_string
    # print(binary_string)
    total += binary_string.count('1')
    for j in range(len(binary_string)):
        if binary_string[j] == '1':
            disk.add((i, j))



print("Part 1", total, len(disk))


G = nx.Graph()
for i, j in disk:
    for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        G.add_node((i, j))
        if (i + di, j + dj) in disk:
            G.add_edge((i, j), (i + di, j + dj))
            # G.add_edge((i, j), ((i + di + 256) % 128, (j + dj + 256) % 128))

print(disk)

print("Part 2", len(list(nx.connected_components(G))))

print(G)


# 1124 too low