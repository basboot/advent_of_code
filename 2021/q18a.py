import math
from itertools import permutations

file1 = open('q18a.txt', 'r')
file_lines = file1.readlines()

homework = []
for line in file_lines:
    homework.append([int(x) if x.isnumeric() else x for x in list(line.rstrip().replace(",", ""))])

def add(left, right):
    return ["["] + left + right + ["]"]

def explode(number):
    last_index = None
    next_index = None
    explode_index = None
    depth = 0

    # find explode point and number before and after it
    for i in range(len(number)):
        if number[i] not in {"[", "]"}:
            if explode_index is None:
                last_index = i
            else:
                if next_index is None:
                    if i > explode_index + 2: # skip exploding numbers
                        next_index = i
        else:
            depth += 1 if number[i] == "[" else -1

            if depth > 4 and explode_index is None:
                explode_index = i

    if explode_index is not None:
        exploded_number = number.copy()
        # add numbers to remove
        if last_index is not None:
            exploded_number[last_index] += exploded_number[explode_index + 1]
        if next_index is not None:
            exploded_number[next_index] += exploded_number[explode_index + 2]
        # remove numbers

        return exploded_number[0:explode_index] + [0] + exploded_number[explode_index + 4:], True
    else:
        return number, False

def split(number):
    # print(number)
    # find split point
    for i in range(len(number)):
        if number[i] not in {"[", "]"} and number[i] > 9:
            half_n = number[i] / 2
            return number[0:i] + ["[", int(math.floor(half_n)), int(math.ceil(half_n)), "]"] + number[i + 1:], True

    return number, False

def reduce(number):
    number, exploded = explode(number)
    if exploded:
        return reduce(number)
    number, splited = split(number)
    if splited:
        return reduce(number)
    return number

def magnitude(numbers):
    while len(numbers) > 1:
        for i in range(len(numbers) - 1):
            # found a pair
            if numbers[i] not in {"[", "]"} and numbers[i + 1] not in {"[", "]"}:
                mag = 3 * numbers[i] + 2 * numbers[i + 1]
                # replace pair with magnitude
                numbers = numbers[0:i-1] + [mag] + numbers[i + 3:]
                break # start over after the list has been altered

    return numbers[0]

# print(explode(homework[0]))
# print(split(["[", 11, 1, "]"]))
# print(reduce(add(homework[0], homework[1])))

result = homework[0]

for i in range(1, len(homework)):
    result = reduce(add(result, homework[i]))

print(result)
print("Part 1", magnitude(result))

max_result = -math.inf
for left, right in permutations(homework, 2):
    max_result = max(max_result, magnitude(reduce(add(left, right))))

print("Part 2", max_result)

