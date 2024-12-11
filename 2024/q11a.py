from collections import defaultdict

file1 = open('q11a.txt', 'r')
lines = file1.readlines()

stones = defaultdict(int)
for stone in list(map(int, lines[0].rstrip().split(" "))):
    stones[stone] += 1

def blink(n_blinks, stones):
    for _ in range(n_blinks):
        new_stones = defaultdict(int)
        for stone, amount in stones.items():
            match stone:
                case 0:
                    new_stones[1] += amount
                case _ if len(str(stone)) % 2 == 0:
                    new_stones[int(str(stone)[0:len(str(stone)) // 2])] += amount
                    new_stones[int(str(stone)[len(str(stone)) // 2:])] += amount
                case _:
                    new_stones[stone * 2024] += amount
        stones = new_stones

    return sum(list(stones.values()))

print(f"Part 1: {blink(25, stones.copy())}")
print(f"Part 2: {blink(75, stones.copy())}")