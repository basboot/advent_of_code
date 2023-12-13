# Using readlines()
file1 = open('q13a.txt', 'r')
lines = file1.readlines()
import numpy as np

puzzle = []
puzzles = []

puzzles_pre_processing  = []

def find_horizontal_mirror_differences(puzzle, n):
    # subtract symmetry, take abs, sum up
    for i in range(len(puzzle) - 1):
        max_comp = min(i + 1, len(puzzle) - i - 1)
        above = puzzle[(i - max_comp + 1):(i + 1),:]
        below = np.flip(puzzle[i+1:i+ 1 + max_comp, :], axis=0)
        differences = np.abs(above - below)
        if np.sum(differences) == n:
            return i + 1 # one indexed in puzzle

    return None

def find_vertical_mirror_differences(puzzle, n):
    # subtract symmetry, take abs, sum up
    for i in range(len(puzzle[0]) - 1):
        max_comp = min(i + 1, len(puzzle[0]) - i - 1)
        above = puzzle[:,(i - max_comp + 1):(i + 1)] # left
        below = np.flip(puzzle[:, i+1:i+ 1 + max_comp], axis=1) # right
        differences = np.abs(above - below)

        if np.sum(differences) == n:
            return i + 1 # one indexed in puzzle

    return None

for line in lines:
    if line.rstrip() == "":
        # print(puzzle)
        np_puzzle = np.array(puzzle)
        puzzles.append(np_puzzle)
        puzzle = []
        continue
    row = [int(x) for x in list(line.rstrip().replace("#", "1").replace(".", "0"))]
    puzzle.append(row)


total = 0
for puzzle in puzzles:
    h_sym, v_sym = find_horizontal_mirror_differences(puzzle, 1), find_vertical_mirror_differences(puzzle, 1)

    if h_sym is not None:
        total += h_sym * 100

    if v_sym is not None:
        total += v_sym

print("Part 2", total)




