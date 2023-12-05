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
for line in lines:
    row = line.rstrip()
    map_row = [c for c in row]
    map_row.append('.') # add extra dot as EOL
    map.append(map_row)


# find numbers by looping through the map
in_number = False # currently in a number?
number_str = "" # to build a number from multiple digits
is_part = False # is current number a partnumber
next_gears = [] # which gears are next to the current number
gears = {} # dict with gear to numbers

total = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        map_cell = map[i][j]
        if in_number:
            if map_cell.isnumeric():
                number_str = number_str + map_cell # build number
                is_part = is_part or is_partnumber((i, j)) # if a symbol has been found it stays a partnumber
                next_gears = next_gears + next_to_gears((i, j)) # store all 'gears' for this number
            else:
                # only partnumbers add to total
                if is_part:
                    total += int(number_str)

                # all numbers can be gears
                for gear in next_gears:
                    if gear in gears:
                        gears[gear].add(int(number_str)) # add number to gear...
                    else:
                        gears[gear] = {int(number_str)} # ...or create new gear in dict for this number

                # reset values for next number
                number_str = ""
                in_number = False
                is_part = False
                next_gears = []
        else:
            # find start of new number
            if map_cell.isnumeric():
                number_str = map_cell
                in_number = True
                is_part = is_partnumber((i, j))
                next_gears = next_gears + next_to_gears((i, j))

print("Part 1", total)


total_gear_ratios = 0
for gear in gears:
    if len(gears[gear]) == 2: # only count gears with two numbers
        g = list(gears[gear])
        ratio = g[0] * g[1]
        total_gear_ratios += ratio

print("Part 2", total_gear_ratios)

# Part 1 514969
# Part 2 78915902