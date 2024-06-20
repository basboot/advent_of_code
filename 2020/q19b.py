import sys

sys.setrecursionlimit(20000)

file1 = open('q19b.txt', 'r')
lines = file1.readlines()

cubes = set()

read_rules = True

rules = {}
messages = []

for i in range(len(lines)):
    line = lines[i].rstrip()

    if line == "":
        read_rules = False
        continue

    if read_rules:
        rule_id = int(line.split(": ")[0])
        rule = [[int(y) if y.isnumeric() else y.replace("\"","") for y in x.split(" ")] for x in line.split(": ")[1].split(" | ")]
        print(rule)
        rules[rule_id] = rule
    else:
        messages.append(list(line))

def is_valid(current_rules, message):
    if len(current_rules) == 0 and len(message) == 0:
        return True

    if len(current_rules) == 0:
        return False
    if len(message) == 0:
        return False

    current_rule = current_rules[0]
    next_rules = current_rules[1:]
    if isinstance(current_rule, int):
        for rule in rules[current_rule]:
            valid = is_valid(rule + next_rules, message)
            if valid:
                return True
        return False
    else:
        if current_rule == message[0]:
            return is_valid(next_rules, message[1:])
        else:
            return False

total = 0
for message in messages:
    print(message)
    if is_valid([0], message):
        print("valid")
        total += 1
    else:
        print("invalid")

print("Valid", total)

# feels like cheating, but rewriting the recursive rules by expanding them for a few recursions works
# 8: 42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42 | 42 42 42 42 42 42
# 11: 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 | 42 42 42 42 42 31 31 31 31 31 | 42 42 42 42 42 42 42 31 31 31 31 31 31 31