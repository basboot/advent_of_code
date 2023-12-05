# Using readlines()
import math

file1 = open('q5a.txt', 'r')
lines = file1.readlines()

# first line contains seeds: 79 14 55 13
seeds = [int(x) for x in lines[0].split(": ")[1].split(" ")]

map_switch = True
map_from = None
map_to = None

mappings = {}

# skip first line with seeds
for i in range(1, len(lines)):
    row = lines[i].rstrip()

    # activate map switch on empty line
    if row == "":
        # print("switch")
        map_switch = True
        continue

    # perform map switch
    if map_switch:
        # input:  seed-to-soil map:
        map_from, map_to = row.replace(" map:", "").split("-to-")
        # print(map_from, map_to)
        map_switch = False
        continue

    # read mapping
    start_range_to, start_range_from, map_range = [int(x) for x in row.split(" ")]
    # print(start_range_to, start_range_from, map_range)

    # add mapping
    if map_from not in mappings:
        mappings[map_from] = {}
        mappings[map_from]["map_to"] = map_to
        mappings[map_from]["mappings"] = []

    mappings[map_from]["mappings"].append((start_range_from, start_range_to, map_range))


def perform_mapping(map_number, map_from):
    # print(f"{map_from} {map_number}")
    # stop when there is no mapping
    if map_from not in mappings:
        return map_number

    # find mapping, if there is any
    for mapping in mappings[map_from]["mappings"]:
        start_range_from, start_range_to, map_range = mapping
        if map_number >= start_range_from and map_number <= start_range_from + map_range:
            # print("match", start_range_from, start_range_to, map_range)
            map_number = start_range_to + (map_number - start_range_from)
            break # only one mapping possible

    # go to next mapping
    # print(f"{mappings[map_from]['map_to']} {map_number}")
    return perform_mapping(map_number, mappings[map_from]["map_to"])

# perform mapping for each seed

lowest = math.inf
for seed in seeds:
    lowest = min(lowest, perform_mapping(seed, "seed"))

print("Part 1", lowest)

lowest = math.inf
for i in range(0, len(seeds), 2):
    first_seed = seeds[i]
    seed_range = seeds[i+1]

    print(first_seed, seed_range)

    for j in range(seed_range + 1):
        lowest = min(lowest, perform_mapping(first_seed + j, "seed"))

print("Part 2", lowest)