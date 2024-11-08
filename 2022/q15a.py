from ast import literal_eval

from scipy.spatial.distance import cityblock

# Using readlines()
file1 = open('q15a.txt', 'r')
lines = file1.readlines()

coverage = {}

BEACON = 1
SENSOR = 2
COVERAGE = 3

def cover_spot(spot, type):
    if spot not in coverage:
        coverage[spot] = type
    else:
        # overwrite coverage with beacon/sensor
        if type != COVERAGE:
            coverage[spot] = type


def cover_area(sensor, beacon):
    cover_spot(sensor, SENSOR)
    cover_spot(beacon, BEACON)

    manhattan_distance = cityblock(sensor, beacon)

    print(manhattan_distance)

    sensor_x, sensor_y = sensor

    for r in range(manhattan_distance + 1):
        for offset in range(r):
            invOffset = r - offset  # Inverse offset
            cover_spot((sensor_x + offset, sensor_y + invOffset), COVERAGE)
            cover_spot((sensor_x + invOffset, sensor_y - offset), COVERAGE)
            cover_spot((sensor_x - offset, sensor_y - invOffset), COVERAGE)
            cover_spot((sensor_x - invOffset, sensor_y + offset), COVERAGE)

for line in lines:
    row = line.rstrip()
    modified_input = row.replace("Sensor at x=", "(").replace(" closest beacon is at x=", "").replace(" y=", "").replace(":", "):(") + ")"
    sensor, beacon = [literal_eval(x) for x in modified_input.split(":")]

    print(sensor, beacon)
    cover_area(sensor, beacon)

count_coverage = 0
for covered_spot in coverage:
    if covered_spot[1] == 10 and coverage[covered_spot] == COVERAGE:
        count_coverage += 1

print("Part 1", count_coverage)

# TODO: solution too slow for real problem, try again

