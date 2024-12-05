from collections import defaultdict

file1 = open('q5a.txt', 'r')
lines = file1.readlines()

before = defaultdict(set)
after = defaultdict(set)
page_ranges = []

read_ordering = True

for line in lines:
    row = line.rstrip()

    # newline separates page ordering and page ranges
    if row == "":
        read_ordering = False
        continue

    if read_ordering:
        left, right = row.split("|")
        after[int(left)].add(int(right))
        before[int(right)].add(int(left))
    else:
        page_ranges.append([int(x) for x in row.split(",")])


def is_correct(n, page_range):
    if n > 0:
        # TODO: optimize by checking set len
        for i in range(n):
            # is anything before that should be after?
            if page_range[i] in after[page_range[n]]:
                return False
    if n < len(page_range) - 1:
        for i in range(n + 1, len(page_range)):
            # is anything after that should be before?
            if page_range[i] in before[page_range[n]]:
                return False
    return True


correct_ranges = []
incorrect_ranges = []

for page_range in page_ranges:
    correct_range = []
    incorrect_range = []

    # separate correct and incorrect placed pages
    for i in range(len(page_range)):
        if is_correct(i, page_range):
            correct_range.append(page_range[i])
        else:
            incorrect_range.append(page_range[i])

    # everything correct => page range was in correct order
    if len(correct_range) == len(page_range):
        correct_ranges.append(correct_range)
        continue

    # move numbers one by one from incorrect to correct
    while len(incorrect_range) > 0:
        # add incorrect number at the end
        correct_range.append(incorrect_range.pop())

        # swap number until it is in the right place
        for i in range(len(correct_range) - 1, -1, -1):
            if is_correct(i, correct_range):
                break
            # not correct, swap
            correct_range[i], correct_range[i-1] = correct_range[i-1], correct_range[i]

    incorrect_ranges.append(correct_range)


print(f"Part 1, {sum(page_range[len(page_range) // 2] for page_range in correct_ranges)}")
print(f"Part 2, {sum(page_range[len(page_range) // 2] for page_range in incorrect_ranges)}")
