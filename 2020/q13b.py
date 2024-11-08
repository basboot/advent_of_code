file1 = open('q13a.txt', 'r')
lines = file1.readlines()


from sympy import Symbol

t = Symbol('t')

raw_ids = lines[1].rstrip().split(",")

ids = []

equations = []

# id_product = 1
for i in range(len(raw_ids)):
    if raw_ids[i] == "x":
        continue
    ids.append((int(raw_ids[i]), i))
    # print(int(raw_ids[i]), isprime(int(raw_ids[i])), i) # all prime numbers
    # id_product *= int(raw_ids[i])

    equations.append(t % int(raw_ids[i]) - i)

    print(f"(t - {i}) mod {int(raw_ids[i])} = 0", end=", ")

print()
# print(equations)

# print(solve(equations, t, dict=True))

# sympy can mod niet oplossen, wolfram wel :-)

# 1249285041610323 + 1463175673841141 n
print(f"Part 2: {1249285041610323 + 1463175673841141}")
print(f"Part 2: {1249285041610323 - 1463175673841141}")
print(f"Part 2: {1249285041610323}")


# CRT opzoeken?
# https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset