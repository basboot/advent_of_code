file1 = open('q14a.txt', 'r')
lines = file1.readlines()

or_mask = 0
and_mask = 2**36 - 1

mem = {}

for line in lines:
    command, value = line.rstrip().split(" = ")
    if command == "mask":
        # print("mask", value)
        or_mask = int(value.replace("X", "0"), 2) # or
        and_mask = int(value.replace("X", "1"), 2) # and
    else:
        address = int(command.replace("mem[", "").replace("]", ""))
        # print("set", address, value)

        unmasked_value = int(value)
        # print(unmasked_value)

        masked_value = (unmasked_value | or_mask) & and_mask

        # print(masked_value)

        mem[address] = masked_value

print(sum(mem.values()))


