file1 = open('q4a.txt', 'r')
lines = file1.readlines()

FIELD_ID = {
    "byr": 0,
    "iyr": 1,
    "eyr": 2,
    "hgt": 3,
    "hcl": 4,
    "ecl": 5,
    "pid": 6,
    "cid": 7
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
        data[FIELD_ID[field]] = 1

all_data.append(data)

print(all_data)

n_valid = 0
for data in all_data:
    if sum(data[0:7]) == 7:
        n_valid += 1

print("Part 1", n_valid)
