# Using readlines()
file1 = open('q11a.txt', 'r')
lines = file1.readlines()

ROUNDS = 20

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
    print(items)
    print(operation, value)
    print(test)
    print(succes, fail)

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

print(monkeys)
print(len(monkeys))

for _ in range(ROUNDS):
    # process each monkey
    for monkey in monkeys:
        # inspect items
        for i in range(len(monkey["items"])):
            print(">>>", monkey)
            # inspects
            monkey["inspected"] += 1
            # increase worry level by monkey
            value = int(monkey["value"]) if monkey["value"] != "old" else monkey["items"][i]
            if monkey["operation"] == "+":
                monkey["items"][i] += value
            else:
                monkey["items"][i] *= value
            # decreaes worry level by third
            monkey["items"][i] = monkey["items"][i] // 3 # divide 3 round down to nearest int

            # throw item to other monkey based on division
            if monkey["items"][i] % monkey["test"] == 0:
                monkeys[monkey["succes"]]["items"].append(monkey["items"][i])
            else:
                monkeys[monkey["fail"]]["items"].append(monkey["items"][i])

        # clear items (all thrown)
        monkey["items"] = []

print(monkeys)

inspects = []
for monkey in monkeys:
    inspects.append(monkey["inspected"])

inspects.sort(reverse=True)
print(inspects)

print(inspects[0] * inspects[1])







