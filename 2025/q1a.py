current = 50
zeros = 0

max_number = 0

with open("q1a.txt") as f:
    for line in f:
        code = line.strip()
        direction, number = code[0], int(code[1:])

        current = (current + number * (1 if direction == "R" else -1)) % 100

        max_number = max(number, max_number)

        if current == 0:
            zeros += 1

print(max_number)


print(f"Part 1: {zeros}")