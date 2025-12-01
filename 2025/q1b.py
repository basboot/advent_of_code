def modulus(n):
    zeros = 0

    while n < 0:
        zeros += 1
        n += 100

    while n > 99:
        zeros += 1
        n -= 100

    return n, zeros


current = 50
zeros = 0

with open("q1a.txt") as f:
    for line in f:
        code = line.strip()
        direction, number = code[0], int(code[1:])

        current, extra_zeros = modulus(current + number * (1 if direction == "R" else -1))

        zeros += extra_zeros

print(f"Part 2: {zeros}")

# 6294 too high


print(modulus(50 + 50))