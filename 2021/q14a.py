file1 = open('q14a.txt', 'r')
file_lines = file1.readlines()

folding_input = False

polymer = list(file_lines[0].rstrip())

rules = {}

for i in range(2, len(file_lines)):
    f, t = file_lines[i].rstrip().split(" -> ")
    rules[tuple(f)] = t

print(polymer)
print(rules)

def grow_polymer(polymer):
    new_polymer = []
    for i in range(len(polymer) - 1): # last cannot be a pair
        f, t = polymer[i], polymer[i + 1] # get pair
        new_polymer.append(f) # first part stays
        if (f, t) in rules: # if there is a rule for this pair, apply
            new_polymer.append(rules[(f, t)])
        # second part of pair will be processed next step

    # add last
    new_polymer.append(polymer[-1])

    return new_polymer


print("".join(polymer))
for i in range(10):
    polymer = grow_polymer(polymer)
    print("".join(polymer))

    # print(len(polymer))

# count parts
counts = {}
for c in polymer:
    if c in counts:
        counts[c] += 1
    else:
        counts[c] = 1
print(counts)


values = list(counts.values())
values.sort()

print("Part 1", values[-1] - values[0])