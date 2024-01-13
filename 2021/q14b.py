file1 = open('q14a.txt', 'r')
file_lines = file1.readlines()

folding_input = False

polymer_string = list(file_lines[0].rstrip())

print("template", polymer_string)

polymer = {}
for i in range(len(polymer_string) - 1):
    f, t = polymer_string[i], polymer_string[i + 1]  # get pair
    if (f, t) in polymer:
        polymer[(f, t)] += 1
    else:
        polymer[(f, t)] = 1


rules = {}

for i in range(2, len(file_lines)):
    f, t = file_lines[i].rstrip().split(" -> ")
    rules[tuple(f)] = ((f[0], t), (t, f[1]))

print(polymer)
print(rules)

def grow_polymer(polymer):
    next_polymer = polymer.copy() # do update in copy to prevent double updates

    for pair in polymer:
        if pair in rules: # some pairs could not have rules
            # remove pair from update
            next_polymer[pair] -= polymer[pair]
            # add new pairs
            for new_pair in rules[pair]:
                if new_pair in next_polymer:
                    next_polymer[new_pair] += polymer[pair]
                else:
                    next_polymer[new_pair] = polymer[pair]

    return next_polymer

def count_chars(polymer):
    # count parts
    counts = {}

    for pair in polymer:
        for c in pair:
            if c in counts:
                counts[c] += polymer[pair]
            else:
                counts[c] = polymer[pair]
        # print(counts)
    return counts


# print("start", polymer)

for i in range(40):
    # print("gen", i)
    polymer = grow_polymer(polymer)
    # print(polymer)



counts = count_chars(polymer)

print(counts)

# all values counted double, except first and last from starting template
counts[polymer_string[0]] += 1
counts[polymer_string[-1]] += 1

print("inc", polymer_string[0], polymer_string[-1])


values = list(counts.values())

print(max(values) / 2, min(values) / 2)

print((max(values) - min(values)) / 2)

# 3605805746074 too low

# 2188189693529

# {'P': 4259, 'S': 3154, 'V': 2354, 'K': 4830, 'C': 4104, 'N': 2743, 'B': 2843, 'H': 5762, 'F': 5840, 'O': 975}
# {'P': 2201, 'K': 2467, 'C': 2181, 'B': 1492, 'F': 3098, 'N': 1491, 'S': 1699, 'H': 3092, 'V': 1222, 'O': 514}

# NBNB
# NOBHNOB
# NCOKBPHBNCOKB
# NNCFOHKVBKPOHCBHNNCFOHKVB