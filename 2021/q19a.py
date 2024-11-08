import numpy as np

# https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
def roll(v): return (v[0],v[2],-v[1])
def turn(v): return (-v[1],v[0],v[2])
def sequence (v):
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield(v)           #    Yield R
            for i in range(3): #    Yield TTT
                v = turn(v)
                yield(v)
        v = roll(turn(roll(v)))  # Do RTR


def all_orientations(scanner):
    sequences = []
    for beacon in scanner:
        sequences.append(sequence(beacon))

    for orientation in zip(*sequences):
        yield np.array(orientation)

file1 = open('q19a.txt', 'r')
file_lines = file1.readlines()

input_scanners = []

input_scanner = set()
for i in range(1, len(file_lines)):
    row = file_lines[i].rstrip()
    if row == "":
        continue
    # print(row)
    if row[0:3] == "---":
        input_scanners.append(input_scanner)
        input_scanner = set()
        continue

    input_scanner.add(tuple([int(x) for x in row.split(",")]))

# add last
input_scanners.append(input_scanner)

print(input_scanners)

result_scanners = []
result_scanners.append((input_scanners.pop(0), np.array([0, 0, 0]))) # choose 0,0,0 as center for first

print(result_scanners)

scanner_to_investigate = 0 # next scanner in result to look at

# 24 orientations
# x, y, z  +/- 8
# x, y, of z boven 3

def all_orientations_bad(scanner):
    for posmin in range(6):
        for above in range(3):
            oriented_scanner = []
            for beacon in scanner:
                # shift 'up'
                x, y, z = [beacon[(n + above) % 3] for n in range(3)]
                x = x if posmin & 4 > 0 else -x
                y = y if posmin & 2 > 0 else -y
                z = z if posmin & 1 > 0 else -z
                oriented_scanner.append((x, y, z))
            yield np.array(oriented_scanner) # TODO: convert to numpy array?

# for orientation in all_orientations([(1, 2, 3), (1, 2, 4)]):
#     # print(orientation)
#     print(set([tuple(x) for x in orientation]))
# exit()
# try to find an orientation + translation for input, that matches target at 12 beacons
def find_match(input, target, target_center):
    np_target = np.array(list(target))

    for np_input_orientation in all_orientations(input):
        # print(np_input_orientation)
        # print("orientation switch")
        for np_input_beacon in np_input_orientation:
            for np_target_beacon in np_target:
                delta = np_target_beacon - np_input_beacon
                # print(delta)

                # translate
                np_translated_input_orientation = np_input_orientation + delta
                # print("in target", np_target_beacon)
                # print("original", np_input_orientation)
                # print("trans", np_translated_input_orientation)

                translated_input_orientation = set([tuple(x) for x in np_translated_input_orientation])

                matches = translated_input_orientation.intersection(target)

                if len(matches) > 11:
                    # print(matches)
                    # # TODO: prevent false positive
                    # print("delta", delta)
                    # np_no_matches_target_distances = np.abs(np.array(list(target - matches)) - delta)
                    # print("target", target_center)
                    # np_no_matches_input_distances = np.abs(np.array(list(translated_input_orientation - matches)) - target_center)
                    #
                    # if np.any(np_no_matches_target_distances) < 1001 or np.any(np_no_matches_input_distances) < 1001:
                    #     print("illegal")
                    # else:
                    print("matches: ", sorted(list(matches)))

                    return True, translated_input_orientation, delta

    return False, set(), None


result_scanner_to_check = 0

while result_scanner_to_check < len(result_scanners):
    print("result scanner", result_scanner_to_check)
    target, target_center = result_scanners[result_scanner_to_check]
    for i in range(len(input_scanners)):
        # print(f"find match for scanner {i}")
        found, result, center = find_match(input_scanners[i], target, target_center)

        if found:
            print(f"found match for scanner {i}, with center {center}")
            # delete input
            input_scanners[i] = set()
            # keep result
            result_scanners.append((result, center))
        else:
            if len(input_scanners[i]) > 0:
                print(f"no found match for scanner {i}, yet")
    # all inputs processed, proceed to next target
    result_scanner_to_check += 1


all_results = set()
centers = []
for scanner, center in result_scanners:
    all_results = all_results.union(scanner)
    centers.append(center)

all_results = list(all_results)
all_results.sort()
print(all_results)
print(len(all_results))


print(centers)




