from ast import literal_eval

from scipy.spatial.distance import cityblock

# Using readlines()
file1 = open('q15a.txt', 'r')
lines = file1.readlines()

sensors = {}
beacons = set()
y_coverage = set() # coverage at one row

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

# def can_beacon_be_present(spot):
#     # ignore occupied spots as in assignment TODO: this is strange
#     if spot in beacons or spot in sensors:
#         return True
#
#     for sensor in sensors:
#         # too close, or same distance which cannot be according to assignment
#         # print(cityblock(sensor, spot), "<=", sensors[sensor], "?")
#         if cityblock(sensor, spot) <= sensors[sensor]:
#             return False
#
#     # not occupied and not too close
#     return True

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

# TODO: solution too slow for part 2, try again