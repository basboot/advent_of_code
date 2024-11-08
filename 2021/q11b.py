from tools.advent_tools import *

file1 = open('q11a.txt', 'r')
lines = file1.readlines()

octopuses, width, height = read_grid(lines, GRID_NUMPY, lambda a: a.strip(), value_conversions=None, int_conversion=True)

STEPS = 100000

print(octopuses)

n_flashes = 0

for n in range(STEPS):
    print("-------- step ", n + 1)
    # print("--- start")
    # print(octopuses)

    # step 1: increase energy by 1
    # print("--- increase")
    octopuses += 1

    # print(octopuses)
    all_flashed_octopuses = octopuses < 0 # create logic matrix filled with False
    # print(all_flashed_octopuses)


    flash_again = True
    while flash_again:
        # print("--- flash")
        flash_again = False
        flashed_octopuses = octopuses > 9 # logic matrix
        flashing_octopuses = np.where(octopuses > 9) # positions

        for (i, j) in zip(flashing_octopuses[0], flashing_octopuses[1]):
            # print(i, j)
            if all_flashed_octopuses[i, j]:  # only flash once
                continue

            n_flashes += 1
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == dj == 0: # don't increase self (though it would not hurt the algorithm)
                        continue
                    if 0 <= i + di < height and 0 <= j + dj < width: # not outside matrix
                        octopuses[i + di, j + dj] += 1
                        flash_again = True # only try to flash again if something changed

        all_flashed_octopuses = all_flashed_octopuses | flashed_octopuses # keep track of who (already) flashed
        # break

        # print(octopuses)
        # print(all_flashed_octopuses)

    # print("--- reset")
    octopuses[all_flashed_octopuses] = 0
    if np.sum(octopuses) == 0:
        print("Steps", n + 1)
        exit()
    # print(octopuses)

print("Flashes", n_flashes)