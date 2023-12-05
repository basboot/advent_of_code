# Using readlines()
file1 = open('q3a.txt', 'r')
lines = file1.readlines()

def is_partnumber(position):
    has_symbol = False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (position[0] + i < 0 or position[1] + j < 0 or
                    position[0] + i > len(map) - 1 or position[1] + j > len(map[0]) - 1):
                # print("outside")
                continue
            # skip numbers
            if map[position[0] + i][position[1] + j].isnumeric():
                # print("too high")
                continue
            # skip dot
            if map[position[0] + i][position[1] + j] == '.':
                continue

            has_symbol = True
    return has_symbol

def next_to_gears(position):
    gears = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (position[0] + i < 0 or position[1] + j < 0 or
                    position[0] + i > len(map) - 1 or position[1] + j > len(map[0]) - 1):
                # print("outside")
                continue
            if map[position[0] + i][position[1] + j] == '*':
                gears.append((position[0] + i, position[1] + j))
    return gears

map = []


i = 0
for line in lines:
    row = line.rstrip()
    # print("input: ", row)

    map_row = []
    j = 0
    for c in row:
        map_row.append(c)

        j += 1
    map_row.append('.') # add extra dot as EOL
    map.append(map_row)
    i += 1

# find numbers
in_number = False
number_str = ""
is_part = False
next_gears = []
gears = {}

total = 0

for i in range(len(map)):
    for j in range(len(map[0])):
        map_cell = map[i][j]
        if in_number:
            if map_cell.isnumeric():
                number_str = number_str + map_cell
                is_part = is_part or is_partnumber((i, j))
                next_gears = next_gears + next_to_gears((i, j))
            else:
                # print(f"number found {number_str}, part {is_part}, gears {next_gears}")
                if is_part:
                    total += int(number_str)

                for gear in next_gears:
                    # print(gear)
                    if gear in gears:
                        gears[gear].add(int(number_str))
                    else:
                        gears[gear] = {int(number_str)}
                number_str = ""
                in_number = False
                is_part = False
                next_gears = []
        else:
            if map_cell.isnumeric():
                number_str = map_cell
                in_number = True
                is_part = is_partnumber((i, j))
                next_gears = next_gears + next_to_gears((i, j))



# print(map)
print("Part 1", total)

# 595217 too high

total_gear_ratios = 0
for gear in gears:
    # print(gears[gear])
    if len(gears[gear]) == 2:
        # print("found", gears[gear])
        g = list(gears[gear])
        ratio = g[0] * g[1]
        total_gear_ratios += ratio

print("Part 2", total_gear_ratios)
