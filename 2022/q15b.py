from ast import literal_eval
from scipy.spatial.distance import cityblock

# Using readlines()
file1 = open('q15a.txt', 'r')
lines = file1.readlines()

covered_areas = [] # use array of tuples so we can sort them
# indexes of tuple
Y = 0
X = 1
MAX_RANGE = 2

sensors = {} # just in case we need the later
beacons = set() # just in case we need the later

for line in lines:
    row = line.rstrip()
    modified_input = row.replace("Sensor at x=", "(").replace(" closest beacon is at x=", "").replace(" y=", "").replace(":", "):(") + ")"
    sensor, beacon = [literal_eval(x) for x in modified_input.split(":")]

    # print(f"sensor at {sensor}, beacon at {beacon} with distance {cityblock(sensor, beacon)}")

    beacons.add(beacon) # beaconpos
    sensors[sensor] = cityblock(sensor, beacon) # sensorpos => distance to beacon

    covered_areas.append((
        sensor[1] + cityblock(sensor, beacon), # max y of covered area
        sensor[0], # x of covered area
        cityblock(sensor, beacon), # max width of covered area
        sensor #center for debugging
         ))

covered_areas.sort(reverse=True) # sort reversed to get y from max to min (default tuples sort on first value)

start_y = covered_areas[0][0] + 1 # start scanning 1 above the highest covered spot

# x and y coordinates each no lower than 0 and no larger than 4000000.
MAX_XY = 4000000

active_intervals = []

LEFT_INTERVAL = 0
RIGHT_INTERVAL = 1
WIDTH = 2
GROWING = 3
MAX_WIDTH = 4
for y in range(start_y, -1, -1):
    # do admin first, then add new
    for i in range(len(active_intervals) -1, -1, -1): # back to front to pop out inactive intervals
        # update intervals and size
        active_intervals[i][LEFT_INTERVAL]  += -1 if active_intervals[i][GROWING] else +1
        active_intervals[i][RIGHT_INTERVAL] += +1 if active_intervals[i][GROWING] else -1
        active_intervals[i][WIDTH] += +1 if active_intervals[i][GROWING] else -1 # single side width

        # size = 0 => inactive
        if active_intervals[i][WIDTH] == 0:
            active_intervals.pop(i)
            continue

        # wil stop growing and start shrinking next round
        if active_intervals[i][WIDTH] == active_intervals[i][MAX_WIDTH] and active_intervals[i][GROWING]:
            active_intervals[i][GROWING] = False

    # activate all areas that come in scope
    while len(covered_areas) > 0 and covered_areas[0][0] == y:
        covered_area = covered_areas.pop(0) # get first, and remove (no active/inactie admin needed)
        active_intervals.append([
            covered_area[X],            # put left interval first for sorting
            covered_area[X],            # right interval (same at start as left)
            1,                          # width (for convenience)
            True,                       # growing, default True
            covered_area[MAX_RANGE] + 1,    # max width + 1 (because we start at 1)
        ])

    # perform check
    # find start 0
    active_intervals.sort()

    # only check within boundaries
    if 0 <= y <= MAX_XY and len(active_intervals) > 0:
        # init first, because we need to have something to compare
        current_interval = active_intervals[0]
        for i in range(len(active_intervals)):
            # exit if there is a gap
            if current_interval[RIGHT_INTERVAL] + 1 < active_intervals[i][LEFT_INTERVAL]:
                # there is a gap #TODO check if gap in area
                if current_interval[RIGHT_INTERVAL] < 0 or active_intervals[i][LEFT_INTERVAL] > MAX_XY:
                    # Gap outside x interval
                    pass
                else:
                    print(f"Gap found at line {y}, between {current_interval[RIGHT_INTERVAL]} and {active_intervals[i][LEFT_INTERVAL]}")
                    x = current_interval[RIGHT_INTERVAL] + 1
                    print(f"Part 2: tuning freq {4000000 * x + y}")
                    exit()

            # update current if next is better
            if active_intervals[i][RIGHT_INTERVAL] > current_interval[RIGHT_INTERVAL]:
                current_interval = active_intervals[i]