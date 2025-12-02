def split_range(start_id, end_id):
    if len(start_id) == len(end_id):
        yield start_id, end_id
    else:
        yield start_id, "9" * len(start_id)
        yield from split_range("1" + "0" * len(start_id), end_id)

def split_number(number_str):
    return int(number_str[0:len(number_str) // 2]), int(number_str[len(number_str) // 2:])

def sum_range(start, end):
    result = 0
    if end < start:
        return 0
    else:
        for n in range(start, end + 1):
            result += int(f"{n}{n}")
    return result


total = 0

with open("q2a.txt") as f:
    id_ranges = f.readline().rstrip().split(",")

    for id_range in id_ranges:
        print("NEW", id_range)
        for start_id, end_id in split_range(*id_range.split("-")):
            assert len(start_id) == len(end_id), "start and end not same length"
            if len(start_id) % 2 == 1:
                continue # ignore odd ranges

            # split both, create both ranges, and check union
            print("CHECK", start_id, end_id)
            min_left, min_right = split_number(start_id)
            max_left, max_right = split_number(end_id)

            # left is leading, so check for each left number if it can be made on the right
            # first, can be made if right min <=
            # last, can be made if right max >=
            # inbetween is never a problem
            min_possible = min_left if min_right <= min_left else min_left + 1
            max_possible = max_left if max_right >= max_left else max_left - 1

            invalid = sum_range(min_possible, max_possible)
            print(invalid)
            total += invalid

print(f"Part 1: {total}") # 40055209690 ok

# 9548853437 too low
# 71026690731 too high

# 3529 9661 3541 1975