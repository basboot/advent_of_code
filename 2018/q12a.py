import matplotlib.pyplot as plt

file1 = open('q12a.txt', 'r')

rules = {}

def apply_rule(pattern):
    if pattern in rules:
        return rules[pattern]
    else:
        assert True, "this should not happen?"
        return " "#pattern[2] # no change

lines = file1.readlines()

state = lines[0].rstrip().replace(".", " ").replace("initial state: ", "")
first_pot = 0

for i in range(2, len(lines)):
    line = lines[i]
    pattern, result = line.rstrip().replace(".", " ").split(" => ")
    rules[pattern] = result


# print(state)
print(rules)



def calc_value(first_pot, state):
    total = 0
    for i in range(len(state)):
        if state[i] == "#":
            total += (first_pot + i)
    return total

gens = [0]
values = [calc_value(first_pot, state)]

for i in range(2000):
    temp = len(state)
    state = state.lstrip()
    first_pot = first_pot - 4 + temp - len(state)
    state = f"    {state.rstrip()}    " # strip to avoid growing too much, add pots before and after for matching
    # print(state)

    next_state = "".join([apply_rule(state[i:i + 5]) for i in range(len(state) - 4)])
    first_pot += 2
    state = next_state

    gens.append(i + 1)
    values.append(calc_value(first_pot, state))

    print(values[-1] - values[-2])



print(first_pot)
print(f"|{state}|")



print(calc_value(first_pot, state))

plt.figure(figsize=(8, 6))
plt.plot(gens, values)

plt.xlabel('gen')
plt.ylabel('value')

plt.show()

# stabalizes after a number og gens adding 69 per gen

# so use value of gen 2000, to calc 50000000000

print(f"after 50000000: {calc_value(first_pot, state) + 69 * (50000000000 - 2000)}")

# 3450002268 too low

# 3450000002268