# Using readlines()
file1 = open('q7a.txt', 'r')
lines = file1.readlines()

# convert cards and types to (hex)values, for easy comparison
# with jokers J is the lowest card => 1
card_to_value = {"A": 0xe, "K": 0xd, "Q": 0xc, "J": 1, "T": 0xa, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
# countings will be sorted, so first two can determine the type
type_to_value = {
    (5, 0): 7,
    (4, 1): 6,
    (3, 2): 5,
    (3, 1): 4,
    (2, 2): 3,
    (2, 1): 2,
    (1, 1): 1
}

hands = []

for line in lines:
    hand, bidding = line.rstrip().split(" ")
    countings = [0] * 16 # we use hex values, so we need some extra space
    value = 0
    assert len(hand) == 5, "We assume all hands have 5 cards"
    for i in range(len(hand)):
        card = hand[i]
        countings[card_to_value[card]] += 1
        value = value << 4 | card_to_value[card] # all values are 0-15, so shift 4 and add to combine

    # use jokers to create a better type
    jokers = countings[card_to_value["J"]]
    countings[card_to_value["J"]] = 0  # remove jokers from countings

    countings.sort(reverse=True) # sort countings, highest first
    countings[0] += jokers  # add jokers to largest count for best hand possible

    type = type_to_value[tuple(countings[0:2])] # after sorting just the first two can determine the type
    value = (type << (5 * 4)) | value

    hands.append((value, int(bidding), hand, type, countings)) # include everything for debugging

hands.sort(reverse=True)

BIDDING = 1

total = 0
for i in range(len(hands)):
    total += (len(hands) - i) * hands[i][BIDDING]

print("Part 2", total)


# 247385181 too low => J is lower than 2

# 247885995