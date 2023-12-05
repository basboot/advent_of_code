from ast import literal_eval

# Using readlines()
file1 = open('q13a.txt', 'r')
lines = file1.readlines()

pairs = []
index = 0

IN_ORDER = 1
OUT_OF_ORDER = -1
INCONCLUSIVE = 0

def in_right_order(left, right):
    # both lists, or list and int
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

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
