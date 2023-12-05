# Using readlines()
import math

file1 = open('q5a.txt', 'r')
lines = file1.readlines()

# first line contains the seed numbers (seeds: 79 14 55 13)
seeds = [int(x) for x in lines[0].split(": ")[1].split(" ")]

map_switch = True # switch to next map
map_from = None
map_to = None

mappings = {}

# skip first line with seeds (already processed), to start with mappings
for i in range(1, len(lines)):
    row = lines[i].rstrip()

    # activate map switch on empty line
    if row == "":
        map_switch = True
        continue

    # perform map switch
    if map_switch:
        # input:  seed-to-soil map:
        map_from, map_to = row.replace(" map:", "").split("-to-")
        map_switch = False
        continue

    # read mapping
    start_range_to, start_range_from, map_range = [int(x) for x in row.split(" ")]

    # add mapping
    if map_from not in mappings:
        mappings[map_from] = {}
        mappings[map_from]["map_to"] = map_to
        mappings[map_from]["mappings"] = []

    mappings[map_from]["mappings"].append((start_range_from, start_range_to, map_range))


def perform_mapping(map_number, map_from):
    # stop when there is no (next) mapping
    if map_from not in mappings:
        return map_number

    # find mapping for this number, if there is any (else just keep same map_number)
    for mapping in mappings[map_from]["mappings"]:
        start_range_from, start_range_to, map_range = mapping
        if map_number >= start_range_from and map_number <= start_range_from + map_range:
            map_number = start_range_to + (map_number - start_range_from)

    # go to next mapping
    return perform_mapping(map_number, mappings[map_from]["map_to"])

# perform mapping for each seed, and find lowest result
lowest = math.inf
for seed in seeds:
    lowest = min(lowest, perform_mapping(seed, "seed"))

print("Part 1", lowest)

# perform mapping for ranges of seeds, and find lowest result
lowest = math.inf
for i in range(0, len(seeds), 2):
    first_seed = seeds[i]
    seed_range = seeds[i+1]

    for j in range(seed_range + 1):
        lowest = min(lowest, perform_mapping(first_seed + j, "seed"))

print("Part 2", lowest)

# TODO: Too slow for large ranges, need other approach => 5b