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


# check all tickets for invalid values
valid_tickets = []
for ticket in tickets:
    valid = True
    for value in ticket:
        if value not in valid_values:
            valid = False
    if valid:
        valid_tickets.append(ticket)

# start with all field on all positions possible
possible_field_mappings = []
for i in range(len(valid_tickets[0])):
    possible_field_mappings.append(set(fields.keys()))

# eliminate illegal mappings
for ticket in valid_tickets:
    for i in range(len(ticket)):
        # check value i on ticket and update mapping i
        value = ticket[i]
        for field in fields:
            if value in fields[field][0] or value in fields[field][1]:
                # mapping is legal, do nothing
                pass
            else:
                # remove illegal mapping
                possible_field_mappings[i].remove(field)



# now use uniqueness of keys to eliminate more mappings (repeat process until no more can be found)
done = False
while not done:
    done = True
    for i in range(len(possible_field_mappings)):
        if len(possible_field_mappings[i]) == 1:
            # unique mapping found, remove mapping from other options
            field = list(possible_field_mappings[i])[0]
            for j in range(len(possible_field_mappings)):
                if i == j:
                    continue # skip self
                if field in possible_field_mappings[j]: # remove mapping if exists
                    possible_field_mappings[j].remove(field)
                    done = False

# multiply values with certain prefix
prefix = "departure"

total = 1
for i in range(len(my_ticket)):
    field = list(possible_field_mappings[i])[0]
    if field.startswith(prefix):
        total *= my_ticket[i]

print(total)