def split_range(start_id, end_id):
    if len(start_id) == len(end_id):
        yield start_id, end_id
    else:
        yield start_id, "9" * len(start_id)
        yield from split_range("1" + "0" * len(start_id), end_id)

with open("q2a.txt") as f:
    id_ranges = f.readline().rstrip().split(",")

    invalid = set()

    for id_range in id_ranges:
        for start_id, end_id in split_range(*id_range.split("-")):

            for n_splits in range(2, 11):
                if len(start_id) % n_splits != 0:
                    continue # ignore unsplittable ranges

                start_range = int(start_id)
                end_range = int(end_id)

                min_left,  max_left = int(start_id[0: len(start_id) // n_splits]), int(end_id[0: len(start_id) // n_splits])

                # try all options
                for i in range(min_left, max_left + 1):
                    # create candidate
                    candidate = int(str(i) * n_splits)
                    if start_range <= candidate <= end_range:
                        invalid.add(candidate)


print(f"Part 2: {sum(invalid)}")

# 46881443412 too low