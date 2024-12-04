import numpy as np
import re

file1 = open('q4a.txt', 'r')

puzzle = np.array([list(row.strip()) for row in file1.readlines()])

def count_xmas(row: []) -> int:
    return len(re.findall(r'XMAS', "".join(row)))


part1:int = 0

for _ in range(4):
    # rows (left right)
    for i in range(len(puzzle)):
        part1 += count_xmas(puzzle[i, :])

    # diags (left top, bottom right)
    for i in range(-len(puzzle) + 1, len(puzzle)):
        part1 += count_xmas(np.diag(puzzle, i))

    # rotate 4 times to get all orientations
    puzzle = np.rot90(puzzle)

print("Part 1", part1)

part2 = 0

for i in range(1, len(puzzle) - 1): # skip boundaries, because the A cannot be there
    for j in range(1, len(puzzle[0]) - 1):
        if puzzle[i, j] == 'A':
            if (puzzle[i - 1, j - 1] == 'M' and puzzle[i + 1, j + 1] == 'S') or (
                    puzzle[i - 1, j - 1] == 'S' and puzzle[i + 1, j + 1] == 'M'):
                if (puzzle[i - 1, j + 1] == 'M' and puzzle[i + 1, j - 1] == 'S') or (
                        puzzle[i - 1, j + 1] == 'S' and puzzle[i + 1, j - 1] == 'M'):
                            part2 += 1

print("Part 2", part2)
