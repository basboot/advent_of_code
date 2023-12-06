import math
import re

# Using readlines()
file1 = open('q6a.txt', 'r')
lines = file1.readlines()

# Time:      7  15   30
times = [int(x) for x in re.sub(' +', ' ', lines[0].rstrip().replace("Time:","").strip()).split(" ")]

# Distance:  9  40  200
distances = [int(x) for x in re.sub(' +', ' ', lines[1].rstrip().replace("Distance:","").strip()).split(" ")]

# Your toy boat has a starting speed of zero millimeters per millisecond.
# For each whole millisecond you spend at the beginning of the race holding down the button,
# the boat's speed increases by one millimeter per millisecond.

# d(istance) = s(peed) * (T - p(ressed_time))
# s = p
# d = p * (T - p)
# d = pT - p^2
# 0 = -p^2 + Tp - d
#
# p = (-T +- sqrt(1+4T))/-2
def find_min_max_race_solutions(t, d):
    det = t * t - 4 * d
    assert det >= 0, "no solution possible"

    solution1 = (-t + math.sqrt(det)) / -2
    # need first integer solution above
    min_p = int(math.floor(solution1 + 1))

    solution2 = (-t - math.sqrt(det)) / -2
    # need first integer solution below
    max_p = int(math.ceil(solution2 - 1))

    assert max_p > min_p, "margin too small for integer result"

    return min_p, max_p

total = 1
for i in range(len(times)):
    min_p, max_p = find_min_max_race_solutions(times[i], distances[i])
    number_of_solutions = max_p - min_p + 1
    total *= number_of_solutions

print("Part 1, ", total)

# Part 2:
single_time = int(re.sub(' ', '', lines[0].rstrip().replace("Time:","").strip()))
single_distance = int(re.sub(' ', '', lines[1].rstrip().replace("Distance:","").strip()))

min_p, max_p = find_min_max_race_solutions(single_time, single_distance)
print(f"Part 2, {max_p - min_p + 1}")

