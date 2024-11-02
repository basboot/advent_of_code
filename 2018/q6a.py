import math
from collections import Counter
import numpy as np

file1 = open('q6a.txt', 'r')

def neighbours(place):
    x, y = place
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        yield x + dx, y + dy

def outside(place, min_x, max_x, min_y, max_y):
    x, y = place
    return x < min_x or x > max_x or y < min_y or y > max_y

places = []
for line in file1.readlines():
    place = [int(x) for x in line.rstrip().split(", ")]
    places.append(place)

xs, ys = zip(*places)

# Find the minimum and maximum for each side
min_x = min(xs)
max_x = max(xs)
min_y = min(ys)
max_y = max(ys)

# init searches
areas = []
for place in places:
    area = {
        "size": 0,
        "frontier": [place],
        "to_add": set(),
        "found": False,
    }
    areas.append(area)


# points itself ar missing, but should not be a problem
total_claimed = {}

# one step

all_found = False
while not all_found:
    all_found = True

    # first select al candidates to grow
    for area in areas:
        if area["found"]:
            continue
        # explore neighbours
        for point in area["frontier"]:
            for neighbour in neighbours(point):
                area["to_add"].add(neighbour)

        # add claims
        for claim in area["to_add"]:
            if claim in total_claimed:
                total_claimed[claim] += 1
            else:
                total_claimed[claim] = 1

    # then add candidates that are only claimed by one area
    for area in areas:
        if area["found"]:
            continue
        all_found = False
        # check if at least one area is still growing not towards infinity
        # reset frontier
        area["frontier"] = []
        inf = True
        for claim in area["to_add"]:
            if not outside(claim, min_x, max_x, min_y, max_y):
                inf = False
            if total_claimed[claim] == 1:
                area["frontier"].append(claim)
                area["size"] += 1

                if not outside(claim, min_x, max_x, min_y, max_y):
                    inf = False

        # stop when only growing towards infinity
        if inf:
            area["size"] = math.inf
            area["frontier"] = []

        if len(area["frontier"]) == 0:
            area["found"] = True

        # reset for next step
        area["to_add"] = set()


areas = sorted(areas, key=lambda x: x['size'] if x['size'] < math.inf else 0, reverse=True)

print(areas)


