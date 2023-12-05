import functools
from ast import literal_eval

# Using readlines()
file1 = open('q13b.txt', 'r')
lines = file1.readlines()

pairs = []
index = 0

IN_ORDER = 1
OUT_OF_ORDER = -1
INCONCLUSIVE = 0

def in_right_order(left, right):
    # print(left, right)
    # print(type(left), type(right))
    # both lists, or list and int
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    # print(left, right)
    for i in range(len(left)):
        # If the right list runs out of items first, the inputs are not in the right orde
        if i == len(right):
            return OUT_OF_ORDER

        # not both ints => check lists
        if isinstance(left[i], list) or isinstance(right[i], list):
            result = in_right_order(left[i], right[i])

            # found solution, return, else check further
            if result in {IN_ORDER, OUT_OF_ORDER}:
                return result
            else:
                continue

        # both integers
        if left[i] < right[i]:
            return IN_ORDER
        if right[i] < left[i]:
            return OUT_OF_ORDER

    # If the left list runs out of items first, the inputs are in the right order
    if len(right) > len(left):
        return IN_ORDER

    # If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
    return INCONCLUSIVE


for i in range(0, len(lines), 3):
    index += 1
    left = literal_eval(lines[i].rstrip())
    right = literal_eval(lines[i+1].rstrip())
    # skip third

    # print(left, right)
    pairs.append({
        "index": index,
        "left": left,
        "right": right
    })

print(pairs)

total = 0
for pair in pairs:
    print(f"Pair {pair['index']} => {in_right_order(pair['left'], pair['right'])}")
    if in_right_order(pair['left'], pair['right']) == 1:
        total += pair['index']

print(f"Part 1, total {total}")

# Part two

# Disregard the blank lines in your list of received packets
packets = []
for pair in pairs:
    packets.append((pair["left"], False)) # False = no divider
    packets.append((pair["right"], False))

# add divider packets
packets.append(([[2]], True))
packets.append(([[6]], True))

# organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.

def compare(item1, item2):
    return in_right_order(item1[0], item2[0])

# print(packets)
packets.sort(key=functools.cmp_to_key(compare), reverse=True)
# print(packets)

decoder_key = 1
for i in range(len(packets)):
    if packets[i][1]: # divider found
        decoder_key *= (i + 1)

print("Part 2", decoder_key)