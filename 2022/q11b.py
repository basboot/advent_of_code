# Using readlines()
file1 = open('q11b.txt', 'r')
lines = file1.readlines()

ROUNDS = 10000

monkeys = []

# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
for i in range(0, len(lines), 7):
    items = [int(x) for x in "".join((lines[i + 1].strip()).split(" ")[2:]).split(",")]
    operation, value = (lines[i + 2].strip()).split(" ")[4:]
    test = int((lines[i + 3].strip()).split(" ")[3])
    succes = int((lines[i + 4].strip()).split(" ")[5])
    fail = int((lines[i + 5].strip()).split(" ")[5])
    # read monkey
    # print(items)
    # print(operation, value)
    # print(test)
    # print(succes, fail)

    monkeys.append({
        "n": i,
        "items": items,
        "operation": operation,
        "value": value,
        "test": test,
        "succes": succes,
        "fail": fail,
        "inspected": 0
    })

# print(monkeys)
# print(len(monkeys))

# find another way to keep your worry levels manageable
modulus = 1
for monkey in monkeys:
    modulus *= monkey["test"]

for round in range(ROUNDS):
    # print(">>>> ROUND: ", round + 1)
    # process each monkey
    for m in range(len(monkeys)):
        # inspect items
        for i in range(len(monkeys[m]["items"])):
            # inspects
            monkeys[m]["inspected"] += 1
            # increase worry level by monkey
            value = int(monkeys[m]["value"]) if monkeys[m]["value"] != "old" else monkeys[m]["items"][i]
            if monkeys[m]["operation"] == "+":
                monkeys[m]["items"][i] += value
            else:
                monkeys[m]["items"][i] *= value

            monkeys[m]["items"][i] = monkeys[m]["items"][i] % modulus
            # decreaes worry level by third
            # monkey["items"][i] = monkey["items"][i] // 3 # divide 3 round down to nearest int

            # throw item to other monkey based on division
            if monkeys[m]["items"][i] % monkeys[m]["test"] == 0:
                monkeys[monkeys[m]["succes"]]["items"].append(monkeys[m]["items"][i])
            else:
                monkeys[monkeys[m]["fail"]]["items"].append(monkeys[m]["items"][i])

        # clear items (all thrown)
        monkeys[m]["items"] = []

        # print(monkeys)

    if (round + 1) % 1000 == 0:
        for i in range(len(monkeys)):
            print(f"{i + 1} inspected {monkeys[i]['inspected']} times")



inspects = []
for monkey in monkeys:
    inspects.append(monkey["inspected"])

inspects.sort(reverse=True)
# print(inspects)

print(inspects[0] * inspects[1])







