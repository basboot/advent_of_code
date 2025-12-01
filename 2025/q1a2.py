current = 50
zeros = 0
extra_zeros = 0

with open("q1a.txt") as f:
    for line in f:
        code = line.strip()
        direction, offset, rounds = 1 if code[0] == "R" else -1, int(code[1:]) % 100, int(code[1:]) // 100
        offset *= direction

        # rounds always add zeros, going over 0 only adds a zero when not coming from 0
        extra_zeros += rounds + (current + offset > 100 or current + offset < 0 if (current > 0) else 0)
        current += offset
        current %= 100

        if current == 0:
            zeros += 1

print(f"Part 1: {zeros}")
print(f"Part 2: {zeros + extra_zeros}")