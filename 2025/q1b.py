def modulus(n):
    result = n

    zeros = 0

    while result < 0:
        zeros += 1
        result += 100

    while result > 99:
        zeros += 1
        result -= 100

    return result, zeros


current = 50
zeros = 0

max_number = 0

with open("q1a.txt") as f:
    for line in f:
        code = line.strip()
        direction, number = code[0], int(code[1:])

        if current == 0 and direction == "L":
            zeros -= 1

        current, extra_zeros = modulus(current + number * (1 if direction == "R" else -1))

        zeros += extra_zeros

        if current == 0 and direction == "L":
            zeros += 1

        print(direction, number, zeros)

print("last: ", current)

print(f"Part 2: {zeros}")

# 6294 too high


# print(modulus(0 + -1))