from collections import defaultdict

splitters = set()
width, height = 0, 0
with open("q7a.txt") as f:
    for i, line in enumerate(f):
        height = max(i, height)
        for j, char in enumerate(line.strip()):
            width = max(width, j)
            if char == "S":
                start = (i, j)
            if char == "^":
                splitters.add((i, j))

width, height = width + 1, height + 1

beams = {start: 1}

has_reached_bottom = False
splits = 0

while True:
    next_beams = defaultdict(int)
    for cell, timelines in beams.items():
        i, j = cell
        if i == height:
            has_reached_bottom = True
            break
        if (i + 1, j) in splitters:
            next_beams[(i + 1, j - 1)] += timelines
            next_beams[(i + 1, j + 1)] += timelines
            splits += 1
        else:
            next_beams[(i + 1, j)] += timelines
    if has_reached_bottom:
        break
    beams = next_beams

print(f"Part 1: {splits}")
print(f"Part 2: {sum(beams.values())}")