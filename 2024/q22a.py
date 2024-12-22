import time
from collections import deque, defaultdict

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

numbers = list(map(int, [line.rstrip() for line in lines]))

prune = 0b111111111111111111111111

def next_number(n):
    n2 = n << 6 # mul 64
    n = n ^ n2 # mix
    n &= prune # prune
    n2 = n >> 5 # div 32
    n = n ^ n2  # mix
    n &= prune  # prune
    n2 = n << 11  # mul 2048
    n = n ^ n2  # mix
    n &= prune  # prune

    return n

total = 0
start_time = time.time()
for n in numbers:
    # print(n)
    for i in range(2000):
        n = next_number(n)
    total += n

print(f"Part 1, {total}")
print(time.time() - start_time)

bananas = defaultdict(int)

for n in numbers:

    ones = n % 10
    changes = deque()
    seen = set()
    for i in range(2000):
        next_n = next_number(n)
        next_ones = next_n % 10

        # print(next_ones)

        change = next_ones - ones
        changes.append(change)

        if len(changes) == 4:
            change_seen = tuple(changes)
            price = next_ones

            if change_seen not in seen: # first seen only counts
                seen.add(change_seen)
                bananas[change_seen] += price

            changes.popleft()

        n = next_n
        ones = next_ones

print("Part 2", max(list(bananas.values())))
print(time.time() - start_time)

# 1.0146770477294922 zonder bitwise
# 0.8194279670715332 met