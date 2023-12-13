# Using readlines()
import math
from dataclasses import dataclass

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

decryption_key = 811589153

zero = None

all_numbers = []
sequence_numbers = []


for i in range(len(lines)):
    value = int(lines[i].rstrip()) * decryption_key

    new_value = (i, value)

    all_numbers.append(new_value)
    sequence_numbers.append(new_value)

    if value == 0:
        assert zero is None, "There should be only one zero"
        zero = new_value


# mix the list of numbers ten times

TIMES_TO_MIX = 10

for _ in range(TIMES_TO_MIX):

    for number_to_move in sequence_numbers:
        # print(number_to_move)


        # move number
        # find pos
        current_pos = all_numbers.index(number_to_move)
        # pop out
        current_number = all_numbers.pop(current_pos)
        # calc new pos
        new_pos = (current_pos + number_to_move[1]) % len(all_numbers)
        # insert back
        all_numbers.insert(new_pos, current_number)

# print("------")
# for n in all_numbers:
#     print(n)

total = 0
for i in range(1, 4): # 4 -3 2
    grove_index = i * 1000 + all_numbers.index(zero)
    # print("G", all_numbers[grove_index % len(all_numbers)])
    total += all_numbers[grove_index % len(all_numbers)][1]

print(total)

# 0x2345
# 012345
