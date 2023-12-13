# Using readlines()
file1 = open('q13a.txt', 'r')
lines = file1.readlines()
import numpy as np

puzzle = []
puzzles = []
for line in lines:
    if line.rstrip() == "":
        # print(puzzle)
        puzzles.append(np.array(puzzle))
        puzzle = []
        continue
    row = [int(x) for x in list(line.rstrip().replace("#", "1").replace(".", "0"))]
    puzzle.append(row)

# print(puzzles)
def are_matching(row_col1, row_col2):
    # might be possible to optimize
    # https://stackoverflow.com/questions/51352527/check-for-identical-rows-in-different-numpy-arrays
    return tuple(row_col1) == tuple(row_col2)

def check_horizonal_symmetry(puzzle):
    # find matching rows first
    for i in range(len(puzzle) - 1):
        if are_matching(puzzle[i,:], puzzle[i + 1,:]):
            # check if other rows also have symmetry
            matching = True
            for i2 in range(i):
                # only check rows inside puzzle
                if 0 <= i - 1 - i2 < len(puzzle) and 0 <= i + 1 + 1 + i2 < len(puzzle):
                    if not are_matching(puzzle[i - 1 - i2,:], puzzle[i + 1 + 1 + i2,:]):
                        matching = False
                        break

            if matching:
                # Assume only one symmetry can exist
                return i + 1 # one indexed in puzzle
    return None


def check_vertical_symmetry(puzzle):
    # find matching rows first
    for i in range(len(puzzle[0]) - 1):
        if are_matching(puzzle[:,i], puzzle[:, i + 1]):
            # check if other rows also have symmetry
            matching = True
            for i2 in range(i):
                # only check rows inside puzzle
                if 0 <= i - 1 - i2 < len(puzzle[0]) and 0 <= i + 1 + 1 + i2 < len(puzzle[0]):
                    if not are_matching(puzzle[:, i - 1 - i2], puzzle[:, i + 1 + 1 + i2]):
                        matching = False
                        break

            if matching:
                # Assume only one symmetry can exist
                return i + 1 # one indexed in puzzle
    return None

total = 0
for puzzle in puzzles:
    h_sym, v_sym = check_horizonal_symmetry(puzzle), check_vertical_symmetry(puzzle)

    if h_sym is not None:
        total += h_sym * 100

    if v_sym is not None:
        total += v_sym

print("Part 1", total)




