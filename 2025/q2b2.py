def split_range(start_id, end_id):
    if len(start_id) == len(end_id):
        yield start_id, end_id
    else:
        yield start_id, "9" * len(start_id)
        yield from split_range("1" + "0" * len(start_id), end_id)

def split_number(left_number_str, right_number_str, n_splits):
    # only create splits if even splits are possible
    splitted_ranges = []
    if len(left_number_str) % n_splits == 0:
        for i in range(n_splits):
            split_len = len(left_number_str) // n_splits
            splitted_ranges.append([
                int(left_number_str[i * split_len:(i + 1) * split_len]),
                int(right_number_str[i * split_len:(i + 1) * split_len])
                ]
            )

    return splitted_ranges

with open("q2a.txt") as f:
    id_ranges = f.readline().rstrip().split(",")

    invalid = set()

    for id_range in id_ranges:
        print("NEW", id_range)
        for start_id, end_id in split_range(*id_range.split("-")):
            print("CHECK", start_id, end_id)

            for n_splits in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
                if len(start_id) % n_splits != 0:
                    continue # ignore unsplittable ranges

                start_range = int(start_id)
                end_range = int(end_id)

                splitted_range = split_number(start_id, end_id, n_splits)
                print(splitted_range)

                min_left,  max_left = splitted_range[0]


                print("LEFT range", min_left, max_left)

                for i in range(min_left, max_left + 1):
                    # create candidate
                    candidate = int(str(i) * n_splits)
                    if candidate >= start_range and candidate <= end_range:
                        invalid.add(candidate)





print(f"Part 2: {sum(invalid)}")

# 46881443412 too low