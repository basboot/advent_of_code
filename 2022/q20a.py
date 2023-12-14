# TODO: probleem is dat de dataclasses geen goed hash ofzo hebben, waardoor de index in de lijst niet
#  altijd klopt als je hem opvraagt via het value

# Using readlines()
import math
from dataclasses import dataclass

file1 = open('q20a.txt', 'r')
lines = file1.readlines()


from dataclasses import dataclass

@dataclass
class Number:
    value: int


cypher = []
initial_cypher = []

zero = None

previous = None
for line in lines:
    value = int(line.rstrip())

    new_number = Number(value=value)
    if value == 0:
        assert zero is None, "More than one ZERO found"
        zero = new_number

    cypher.append(new_number)
    initial_cypher.append(new_number)

# cypher: array to 'decrypt'
# initial_cypher: original order

dummy = None

for number_to_move in initial_cypher:

    current_pos = cypher.index(number_to_move)

    print(number_to_move)
    print("pos", current_pos)

    # value = cypher.pop(current_pos)
    # cypher.insert(current_pos, dummy)
    #
    # new_pos = (current_pos + value.value + 1) % len(cypher)
    # cypher.insert(new_pos % len(cypher), value)
    #
    # dummy_pos = cypher.index(dummy)
    # _ = cypher.pop(dummy_pos)


total = 0
for i in range(1, 4): # 4 -3 2
    grove_index = i * 1000 + cypher.index(zero)
    print("G", cypher[grove_index % len(cypher)])
    total += cypher[grove_index % len(cypher)].value

# 0x2345
# 012345


print("total", total)
