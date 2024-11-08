from itertools import product

file1 = open('q22a.txt', 'r')
file_lines = file1.readlines()

cubes = []
for line in file_lines:
    onoff, values = line.rstrip().split(" ")

    ranges = [([int(x) for x in range.split("..")]) for range in values.replace("x=","").replace("y=","").replace("z=","").split(",")]

    cubes.append((1 if onoff == "on" else 0, ranges))

print(cubes)

def get_overlap(interval1, interval2):
    # put in right order
    if interval2[0] < interval1[0]:
        return get_overlap(interval2, interval1)

    # no overlap
    if interval1[1] < interval2[0]:
        return None

    before = None if interval1[0] == interval2[0] else (interval1[0], interval2[0] - 1)
    overlap = (interval2[0], min(interval1[1], interval2[1]))
    after = None if interval1[1] == interval2[1] else (min(interval2[1], interval1[1]) + 1, max(interval2[1], interval1[1]))
    return before, overlap, after

# print(get_overlap([1, 10], [5, 25]))

def get_intersection(cube1, cube2):
    intersection = []
    for axis in range(3):
        overlap = get_overlap(cube1[axis], cube2[axis])
        if overlap is None:
            return None
        else:
            intersection.append(overlap[1]) # only need the overlap, ignore before and after

    return tuple(intersection)
def remove_intersection(cube, intersection):
    print("Test cube: ", cube)
    print("Test intersection: ", intersection)
    ranges = []
    for axis in range(3):
        r = []
        before, overlap, after = get_overlap(cube[axis], intersection[axis])
        if before is not None:
            r.append(before)
        if overlap is not None:
            r.append(overlap)
        if after is not None:
            r.append(after)
        ranges.append(r)

    print("----", ranges)

    new_cubes = []
    for new_cube in product(*ranges):

        if tuple(new_cube) == intersection:
            print("don't add intersection")
            continue # remove intersection
        print("ADD", new_cube)
        new_cubes.append(new_cube)

    return new_cubes


cuboid = []

for onoff, cube in cubes:
    next_cuboid = []

    # print(onoff, cube)
    for part in cuboid:
        intersection = get_intersection(cube, part)
        if intersection is None:
            # no intersaction, so part stays intact
            next_cuboid.append(part)
        else:
            # intersection, so remove intersection from part to avoid double counting
            print(f"intersection {intersection}")

            for new_part in remove_intersection(part, intersection):
                print("NEW", new_part)
                next_cuboid.append(new_part)

    # only add next cube if it is 'on'
    if onoff == 1:
        next_cuboid.append(cube)

    cuboid = next_cuboid

total = 0
for x, y, z in cuboid:
    volume = (abs(x[0] - x[1]) + 1) * (abs(y[0] - y[1]) + 1) * (abs(z[0] - z[1]) + 1)
    total += volume
print("Part 2", total)


