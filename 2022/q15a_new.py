from ast import literal_eval
from scipy.spatial.distance import cityblock

# Using readlines()
file1 = open('q15a.txt', 'r')
lines = file1.readlines()

sensors = {}

beacons = set()

y_coverage = set()

def add_y_coverage(sensor, y):
    added_range = sensors[sensor] - abs(sensor[1] - y)
    print(added_range)

    for i in range(added_range + 1): # check + 1
        lp = (sensor[0] - i, y)
        rp = (sensor[0] + i, y)

        if lp not in beacons and lp not in sensors:
            y_coverage.add(lp)
        if rp not in beacons and rp not in sensors:
            y_coverage.add(rp)

def can_beacon_be_present(spot):
    # ignore occupied spots as in assignment TODO: this is strange
    if spot in beacons or spot in sensors:
        return True

    for sensor in sensors:
        # too close, or same distance which cannot be according to assignment
        # print(cityblock(sensor, spot), "<=", sensors[sensor], "?")
        if cityblock(sensor, spot) <= sensors[sensor]:
            return False

    # not occupied and not too close
    return True


for line in lines:
    row = line.rstrip()
    modified_input = row.replace("Sensor at x=", "(").replace(" closest beacon is at x=", "").replace(" y=", "").replace(":", "):(") + ")"
    sensor, beacon = [literal_eval(x) for x in modified_input.split(":")]

    # print(sensor, beacon)
    sensors[sensor] = cityblock(sensor, beacon)
    beacons.add(beacon)


y = 2000000

for sensor in sensors:
    print(sensor)
    add_y_coverage(sensor, y)


l =list(y_coverage)
l.sort()

MAX_X = 4000000
for x in range(MAX_X + 1):
    if (x, y) not in l:
        print("Found")

print(l)


print("Part 2", len(y_coverage))

# 5011718 too low => opnieuw beginnen
# y = 2000000
#
# count = 0
# for x in range(10000000):
#     if not can_beacon_be_present((x, y)):
#         count += 1
#     if x > 0: # avoid double count
#         if not can_beacon_be_present((-x, y)):
#             count += 1
#
#     if x % 1000 == 0:
#         print(count)

# print(can_beacon_be_present((1, 10)))
# count_coverage = 0
# for covered_spot in coverage:
#     if covered_spot[1] == 10 and coverage[covered_spot] == COVERAGE:
#         count_coverage += 1
#
# print("Part 1", count_coverage)

