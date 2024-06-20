file1 = open('q14a.txt', 'r')
lines = file1.readlines()

mem = {}

and_mask = 2**36 - 1

def find_x(mask):
    xs = []
    mask = list(mask)
    mask.reverse()
    for i in range(len(mask)):
        if mask[i] == "X":
            xs.append(i)
    return xs

base_mask = 0 # init no mask
xs = []
for line in lines:
    command, value = line.rstrip().split(" = ")
    if command == "mask":
        # print("mask", value)
        xs = find_x(value)
        base_mask = int(value.replace("X", "0"), 2)

        # print(base_mask, xs)
    else:
        address = int(command.replace("mem[", "").replace("]", ""))
        # print("set", address, value)

        # always perform basemask
        addresses = { address | base_mask }

        # optional floating bits
        for x in xs:
            new_addresses = set()
            for address in addresses:
                new_addresses.add(address | (1 << x))
                new_addresses.add(address & ~(1 << x))
            addresses = new_addresses

        # print(addresses)

        for address in addresses:
            mem[address] = int(value)

total = 0
for address in mem:
    total += mem[address]

print("Part 2", total)



