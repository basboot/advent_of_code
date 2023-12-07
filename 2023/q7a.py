# Using readlines()
file1 = open('q7a.txt', 'r')
lines = file1.readlines()

# convert cards and types to (hex)values, for easy comparison
card_to_value = {"A": 0xe, "K": 0xd, "Q": 0xc, "J": 0xb, "T": 0xa, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
# card countings will be sorted, so first two can determine the type
type_to_value = {
    (5, 0): 7,
    (4, 1): 6,
    (3, 2): 5, # full house
    (3, 1): 4,
    (2, 2): 3, # two pair
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

    countings.sort(reverse=True) # sort countings, highest first
    type = type_to_value[tuple(countings[0:2])] # after sorting just the first two can determine the type
    value = (type << (5 * 4)) | value
    hands.append((value, int(bidding), hand, type, countings)) # include everything for debugging

# sort hands to value, to find ranks
hands.sort(reverse=True)

# count rank * bidding
BIDDING = 1
total = 0
for i in range(len(hands)):
    total += (len(hands) - i) * hands[i][BIDDING]
print("Part 1", total)


