import math
from functools import reduce
import operator

reduce(operator.mul, (3, 4, 5), 1)

file1 = open('q16a.txt', 'r')
file_lines = file1.readlines()

hex_string = file_lines[0].rstrip()

print(hex_string)

# convert to bits
transmission_int = int(hex_string, 16)
transmission_bits = bin(transmission_int)[2:] # remove 0b
print(transmission_bits)
n_bits = len(hex_string) * 4
print(n_bits)

# restore leading zeros
while len(transmission_bits) < n_bits:
    transmission_bits = "0" + transmission_bits

assert n_bits == len(transmission_bits), "something went wrong, we lost some bits"


# return value and length
def read_literal(transmission, position):
    value = ""
    has_next = True

    while has_next:
        has_next = True if transmission[position] == '1' else False
        value = value + transmission[position + 1: position + 5]
        position += 5

    return int(value, 2), 5 * len(value) // 4

def read_operator15(transmission, position):
    bits_in_sub_packets = int(transmission[position:position + 15], 2)


    position += 15
    end_position = position + bits_in_sub_packets

    values = []

    while position < end_position:
        value, position = read_packet(transmission, position)
        values.append(value)

    return values, 15 + bits_in_sub_packets
def read_operator11(transmission, position):
    number_of_sub_packets = int(transmission[position:position + 11], 2)

    position += 11
    start_position = position
    values = []
    for i in range(number_of_sub_packets):
        value, position = read_packet(transmission, position)
        values.append(value)

    # TODO: read values
    return values, 11 + (position - start_position)
def read_operator(transmission, position):
    # first bits selects type 0 => 15, 1 => 11
    if transmission[position] == '0':
        values, n_bits = read_operator15(transmission, position + 1)
    else:
        values, n_bits = read_operator11(transmission, position + 1)

    return values, n_bits + 1

# def calc_bit_size(n_bits):
#     # find nearest multiple of 4 to include trailing zeros
#     return int(4 * math.ceil(n_bits / 4))

sum_version_numbers = 0

# return packet and position of next
def read_packet(transmission, position):
    global sum_version_numbers
    version = int(transmission[position:position + 3], 2)
    sum_version_numbers += version

    id = int(transmission[position + 3:position + 6], 2)

    if id == 4: # 4 is literal, all others are operators
        payload, n_bits = read_literal(transmission, position + 6)
        value = payload
    else:
        payload, n_bits = read_operator(transmission, position + 6)

        match id:
            case 0:
                value = sum(payload)
            case 1:
                value = reduce(operator.mul, payload, 1)
            case 2:
                value = min(payload)
            case 3:
                value = max(payload)
            case 5:
                assert len(payload) == 2, "greater than must have exactly 2 parameters"
                value = 1 if payload[0] > payload[1] else 0
            case 6:
                assert len(payload) == 2, "less than must have exactly 2 parameters"
                value = 1 if payload[0] < payload[1] else 0
            case 7:
                assert len(payload) == 2, "equal must have exactly 2 parameters"
                value = 1 if payload[0] == payload[1] else 0
            case _:
                assert True, "operator not implemented"

    packet_size = 6 + n_bits

    return value, position + packet_size


result, _ = read_packet(transmission_bits, 0)

print("Part 1", sum_version_numbers)

print("Part 2", result)

# documentation

# literal packet
# - 3 bits, version
# - 3 bits, id  (4 = literal)
# - n x 5 bits 1/0, 0 is last, xxxx number
# - trailing zeros, to fit in hex (total must be multiple of 4 bits)

# operator packet type 0
# - 3 bits, version
# - 3 bits, id (not 4 = operator)
# - 1 bit (0 = 15 bit next)
# - 15 bits, containing number n
# - n bits, containing two numbers (not clear how devided...)
# - trailing zeros, to fit in hex (total must be multiple of 4 bits)

# operator packet type 0
# - 3 bits, version
# - 3 bits, id (not 4 = operator)
# - 1 bit (1 = 11 bit next)
# - 11 bits, containing number n
# - n times 11 bits, containing n numbers
# - trailing zeros, to fit in hex (total must be multiple of 4 bits)

# examples:
# 8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
# 620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
# C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
# A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.