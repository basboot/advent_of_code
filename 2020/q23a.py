file1 = open('q23a.txt', 'r')
lines = file1.readlines()

cups = [int(x) for x in list(lines[0].rstrip())]

# print(cups)
max_cup = len(cups)

def pop_three_cups(current_cup, cups):
    cup_to_pop = current_cup + 1
    popped_cups = []
    for i in range(3):
        if cup_to_pop >= len(cups):
            cup_to_pop = 0
        popped_cups.append(cups.pop(cup_to_pop))

    return popped_cups

def find_location_to_insert(value, cups):
    index = None
    while index is None:
        try:
            index = cups.index(value)
            print(f"found label {value}")
        except:
            value = value - 1
            if value < 1:
                value = max_cup
    return index

current_cup = 0

for i in range(100):
    current_label = cups[current_cup]
    print(cups, f"({current_label})")
    popped_cups = pop_three_cups(current_cup, cups)
    print(popped_cups)
    print("<", cups)
    location = find_location_to_insert(current_label - 1, cups)
    print(location + 1)
    print("----")
    cups = cups[0:location + 1] + popped_cups + cups[location + 1:]



    current_cup = cups.index(current_label) + 1
    if current_cup >= max_cup:
        current_cup = 0


# rearrange
cup1 = cups.index(1)
cups = cups[cup1:] + cups[0:cup1]
print(cups)

print("".join([str(x) for x in cups[1:]]))