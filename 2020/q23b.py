file1 = open('q23a.txt', 'r')
lines = file1.readlines()

cups = [int(x) for x in list(lines[0].rstrip())]

n_cups = 1000000
cups = cups + list(range(len(cups) + 1, n_cups + 1))
# print(cups)

# create list label -> next_label (skip 0 for convenience)
next_cups = [0] * (len(cups) + 1)
for i in range(len(cups) - 1):
    next_cups[cups[i]] = cups[i+1]
next_cups[cups[-1]] = cups[0]

def get_destination(current_label, illegal_labels):
    while True:
        # minus one, with wrap around
        current_label = (current_label - 1) if current_label > 1 else len(cups)
        # select only if label is allowed
        if current_label not in illegal_labels:
            return current_label



current_cup = cups[0]

for n in range(10000000):

    cups_to_move = next_cups[current_cup], next_cups[next_cups[current_cup]], next_cups[next_cups[next_cups[current_cup]]]

    after_gap = next_cups[next_cups[next_cups[next_cups[current_cup]]]]

    # print(current_cup)
    # print(cups_to_move)


    destination = get_destination(current_cup, cups_to_move)
    # print(destination)

    after_destination = next_cups[destination]

    next_cups[destination] = next_cups[current_cup]
    next_cups[next_cups[next_cups[next_cups[current_cup]]]] = after_destination
    next_cups[current_cup] = after_gap

    current_cup = next_cups[current_cup]

current = 1
cups_after_one = []
for i in range(len(cups) - 1):
    current = next_cups[current]
    cups_after_one.append(current)

# print("Part 1", cups_after_one)

print(f"Part 2 {cups_after_one[0] * cups_after_one[1]}")






