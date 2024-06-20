file1 = open('q16a.txt', 'r')
lines = file1.readlines()

fase = 0

fields = {}
my_ticket = None
other_tickets = []

for line in lines:
    row = line.rstrip()

    if row == "your ticket:":
        fase = 1
        continue

    if row == "nearby tickets:":
        fase = 2
        continue

    if row == "":
        continue

    match (fase):
        case 0:
            field, values = row.split((": "))
            ranges = [[int(y) for y in x.split("-")] for x in values.split(" or ")]
            fields[field] = [set(range(ranges[0][0], ranges[0][1] + 1)), set(range(ranges[1][0], ranges[1][1] + 1))]
        case 1:
            my_ticket = [int(x) for x in row.split(",")]
        case 2:
            other_tickets.append([int(x) for x in row.split(",")])

# combine all valid ranges in one set
valid_values = set()
for ranges in fields.values():
    valid_values = valid_values.union(ranges[0])
    valid_values = valid_values.union(ranges[1])

# combine tickets
tickets = other_tickets + [my_ticket]

total = 0
# check all tickets for invalid values
for ticket in tickets:
    for value in ticket:
        if value not in valid_values:
            total += value

print(total)

