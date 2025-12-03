joltage = 0

with open("q3a.txt") as f:
    for line in f:
        batteries = list(map(int, list(line.strip())))
        left = max(batteries)

        # corner case, largest is the last
        left_idx = batteries.index(left)

        if left_idx == len(batteries) - 1:
            right = left
            left = max(batteries[0:left_idx])
        else:
            right = max(batteries[left_idx + 1:])

        print(left, right)

        joltage += 10 * left + right


print(f"Part 1: {joltage}")

