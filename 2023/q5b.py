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

    # add mapping
    if map_from not in mappings:
        mappings[map_from] = {}
        mappings[map_from]["map_to"] = map_to
        mappings[map_from]["mappings"] = []

    mappings[map_from]["mappings"].append((start_range_from, start_range_to, map_range))

def perform_range_mapping(number_ranges, map_from_type): # map_number_ranges [[first, last], [first, last]]
    # stop when there is no mapping
    if map_from_type not in mappings:
        return number_ranges

    # find mapping, if there is any
    number_ranges_to_process = number_ranges.copy()
    number_ranges_processed = []

    for mapping in mappings[map_from_type]["mappings"]:
        number_ranges_to_re_process = []
        for number_range_to_process in number_ranges_to_process:
            number_range_start, number_range_end = number_range_to_process

            mapping_range_start_from, mapping_range_start_to, mapping_range = mapping

            mapping_lowest_number = mapping_range_start_from
            mapping_highest_number = mapping_range_start_from + mapping_range - 1
            mapping_offset = mapping_range_start_to - mapping_range_start_from

            # part that is too low to process (if there is any)
            if number_range_start < mapping_lowest_number:
                number_ranges_to_re_process.append((number_range_start, min(mapping_lowest_number - 1, number_range_end)))

            # part that can be mapped
            if number_range_start <= mapping_highest_number and number_range_end >= mapping_lowest_number:
                number_ranges_processed.append((max(number_range_start, mapping_lowest_number) + mapping_offset, min(number_range_end, mapping_highest_number) + mapping_offset))

            # part that is too high to process
            if number_range_end > mapping_highest_number:
                number_ranges_to_re_process.append((max(number_range_start, mapping_highest_number + 1), number_range_end))

        # reprocess in next mapping
        number_ranges_to_process = number_ranges_to_re_process

    result = number_ranges_processed + number_ranges_to_process

    # go to next mapping
    return perform_range_mapping(result, mappings[map_from_type]["map_to"])

# perform seed mappings on ranges and find lowest result
lowest = math.inf
for i in range(0, len(seeds), 2):
    first_seed = seeds[i]
    seed_range = seeds[i+1]

    results = perform_range_mapping ([(first_seed, first_seed + seed_range - 1)], "seed")

    for result in results:
        lowest = min(lowest, result[0]) # first value is smallest of range, no need to compare others

print("Part 2", lowest)