from collections import Counter

start, end = [int(x) for x in "372037-905157".split("-")]

print(start, end)

total = 0
total2 = 0
for password in range(start, end + 1):
    if sorted(list(str(password))) == list(str(password)):
        if 2 in Counter(list(str(password))).values():
            total2 += 1

        if any([x >= 2 for x in Counter(list(str(password))).values()]):
            total += 1

# 377777 too high?

print("Part 1", total)
print("Part 2", total2)