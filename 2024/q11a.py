from collections import defaultdict

file1 = open('q11a.txt', 'r')
lines = file1.readlines()

stones = defaultdict(int)
for stone in list(map(int, lines[0].rstrip().split(" "))):
    stones[stone] += 1

N_BLINKS = 75

for _ in range(N_BLINKS):
    new_stones = defaultdict(int)
    for stone, amount in stones.items():

        if stone == 0:
            new_stones[1] += amount
            continue

        str_stone = str(stone)
        len_stone = len(str_stone)
        if len_stone % 2 == 0:
            new_stones[int(str_stone[0:len_stone // 2])] += amount
            new_stones[int(str_stone[len_stone // 2:])] += amount
            continue

        new_stones[stone * 2024] += amount

    stones = new_stones

print(f"Part 1, {sum(list(stones.values()))}")
