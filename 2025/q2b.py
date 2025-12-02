import math


def split_range(start_id, end_id):
    if len(start_id) == len(end_id):
        yield start_id, end_id
    else:
        yield start_id, "9" * len(start_id)
        yield from split_range("1" + "0" * len(start_id), end_id)

def split_number(left_number_str, right_number_str, n_splits):
    # only create splits if even splits are possible
    if len(left_number_str) % n_splits == 0:
        for i in range(n_splits - 1):
            split_len = len(left_number_str) // n_splits
            yield int(left_number_str[i * split_len:(i + 1) * split_len]), int(left_number_str[(i + 1) * split_len:(i + 2) * split_len]), int(right_number_str[i * split_len:(i + 1) * split_len]), int(right_number_str[(i + 1) * split_len:(i + 2) * split_len])
    else:
        return

def sum_range(start, end, n_splits):
    result = 0
    if end < start:
        return 0
    else:
        n_digits = len(str(start))
        illegal_combinations = set()
        if n_splits in {3, 5} and n_digits == 2:
            for n in range(1, 10):
                illegal_combinations.add(int(n_digits * str(n)))
            print(">>> Illegal", illegal_combinations)
        for n in range(start, end + 1):
            if n in illegal_combinations:
                continue # skip to avoid double count
            result += int(f"{n}" * n_splits)
    return result

def find_overlap(min_left, min_right, max_left, max_right):
    # left is leading, so check for each left number if it can be made on the right
    # first, can be made if right min <=
    # last, can be made if right max >=
    # inbetween is never a problem
    min_possible = min_left if min_right <= min_left else min_left + 1
    max_possible = max_left if max_right >= max_left else max_left - 1

    return min_possible, max_possible

total = 0

with open("q2a.txt") as f:
    id_ranges = f.readline().rstrip().split(",")

    for id_range in id_ranges:
        print("NEW", id_range)
        for start_id, end_id in split_range(*id_range.split("-")):
            assert len(start_id) == len(end_id), "start and end not same length"

            # split both, create both ranges, and check union
            print("CHECK", start_id, end_id)

            for n_splits in [2, 3, 5, 7]:
                if len(start_id) % n_splits != 0:
                    continue # ignore unsplittable ranges

                print("Check split", n_splits)
                min_possible, max_possible = 0, 9999999999
                for min_left, min_right, max_left, max_right in split_number(start_id, end_id, n_splits):
                    min_p, max_p = find_overlap(min_left, min_right, max_left, max_right)
                    min_possible = max(min_p, min_possible)
                    max_possible = min(max_p, max_possible)

                invalid = sum_range(min_possible, max_possible, n_splits)
                print("Possible: ", min_possible, max_possible)
                print("I", invalid)
                total += invalid

print(f"Part 2: {total}")

# 46881443412 too low