file1 = open('q4a.txt', 'r')
lines = file1.readlines()

import re

# TODO: add min + max check, including strange case for hgt

FIELD_SETTINGS = {
    "byr": (0, "\d{4}", 1920, 2002),
    "iyr": (1, "\d{4}", 2010, 2020),
    "eyr": (2, "\d{4}", 2020, 2030),
    "hgt": (3, "\d+(cm|in)", (150, 59), (193, 76)),
    "hcl": (4, "#[0-9a-f]{6}", None, None),
    "ecl": (5, "(amb|blu|brn|gry|grn|hzl|oth)", None, None),
    "pid": (6, "\d{9}", None, None),
    "cid": (7, "", None, None)
}

all_data = []

data = [0] * 8

for line in lines:
    row = line.rstrip()
    if row == "":
        print("---")
        print(data)
        all_data.append(data)
        data = [0] * 8
        continue
    pairs = [x.split(":") for x in row.split(" ")]

    for field, value in pairs:
        id, pattern, lowest, highest = FIELD_SETTINGS[field]
        print(value, end=" ")
        if re.fullmatch(pattern, value) is None:
            print("no match")
        else:
            print("match")
            # TODO: check value
            if lowest is not None: # need to check value
                # special case, adjust value, min and max
                if field == "hgt":
                    if value[-2:] =="cm":
                        value = value[:-2]
                        lowest = lowest[0]
                        highest = highest[0]
                    else:
                        value = value[:-2]
                        lowest = lowest[1]
                        highest = highest[1]
                value = int(value)

                if value < lowest or value > highest:
                    continue

            data[id] = 1

all_data.append(data)

print(all_data)

n_valid = 0
for data in all_data:
    if sum(data[0:7]) == 7:
        n_valid += 1

print("Part 2", n_valid)

# 130 too low