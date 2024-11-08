illegal = [ord(x) - ord('a') for x in list("iol")]
start = [ord(x) - ord('a') for x in list("vzbxxyzz")]

# ChatGPT
def has_three_consecutive_increasing(nums):
    count = 1  # Initialize count of consecutive increasing numbers

    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:  # Check if current number is greater than the previous
            count += 1  # Increment count for a consecutive increase
            if count >= 3:  # If we have at least three consecutive increases
                return True
        else:
            count = 1  # Reset count if the sequence breaks

    return False  # No sequence of three consecutive increases found


def has_two_distinct_adjacent_pairs(nums):
    n_pairs = 0
    last_pair = -2
    pairs = set()
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            if last_pair < i:
                if nums[i] not in pairs:
                    n_pairs += 1
                    pairs.add(nums[i])
                last_pair = i + 2
            else:
                n_pairs -= 1
                last_pair = i + 2
    return n_pairs == 2

def skip_illegal(n):
    illegal_found = False
    for i in range(len(n)):
        if illegal_found:
            n[i] = 0
        else:
            if n[i] in illegal:
                n[i] += 1
                illegal_found = True

    return n

def add_one(n, digit = 0):
    pos = len(n) - digit - 1
    if n[pos] == 25:
        n[pos] = 0
        return add_one(n, digit + 1)
    else:
        n[pos] += 1
        return n

n = start

while True:
    n = add_one(n)
    n = skip_illegal(n)
    if has_three_consecutive_increasing(n) and has_two_distinct_adjacent_pairs(n):
        print("".join([chr(x + ord('a')) for x in n]))
        exit()

