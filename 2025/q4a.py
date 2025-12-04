width = 0
height = 0

grid = set()

with open("q4a.txt") as f:
    for i, line in enumerate(f):
        for j, cell in enumerate(list(line.strip())):
            width = max(j, width)
            height = max(i, height)
            if cell == "@":
                grid.add((i, j))

def adjacent_rolls(i, j):
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue # ignore self
            ni = i + di
            nj = j + dj

            if (ni, nj) in grid:
                count += 1
    return count


def get_removable_rolls():
    removable = set()
    for cell in grid:
        if adjacent_rolls(*cell) < 4:
            removable.add(cell)
    return removable


print(f"Part 1: {len(get_removable_rolls())}")

total_rolls = len(grid)

while True:
    removable = get_removable_rolls()
    if len(removable) == 0:
        break
    grid = grid - removable

print(f"Part 2: {total_rolls - len(grid)}")