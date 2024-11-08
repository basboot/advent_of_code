from functools import reduce

file1 = open('q10a.txt', 'r')
lengths = [ord(x) for x in file1.readlines()[0].rstrip()]
lengths += [17, 31, 73, 47, 23]


SIZE = 256

list = list(range(SIZE))


position = 0
skip_size = 0

length = lengths[0]

def swap_list(start, length, list):
    for i in range(length // 2):
        temp = list[(start + i) % SIZE]
        list[(start + i) % SIZE] = list[(start + length - i - 1) % SIZE]
        list[(start + length - i - 1) % SIZE] = temp

print(list)

for _ in range(64): # 64x
    for length in lengths:
        swap_list(position, length, list)
        position = (position + length + skip_size) % SIZE
        print(position)
        print(list)
        skip_size += 1

# now xor

result = ""
for i in range(16):
    result += (format(reduce(lambda i, j: int(i) ^ int(j), list[i * 16: (i + 1) * 16]), 'x').zfill(2))

print("Part 2", result)

# 63756 too high
# 11413