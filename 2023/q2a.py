# Using readlines()
file1 = open('q2a.txt', 'r')
lines = file1.readlines()

# maximum allowed per color
RED = 12
GREEN = 13
BLUE = 14

# check if hand is possible within color limits
def is_possible(hands):
    for hand in hands:
        if hand["red"] > RED or hand["blue"] > BLUE or hand["green"] > GREEN:
            return False
    return True

# calculate the power of a hand by multiplying the max for each color
def power(hands):
    red = 0
    green = 0
    blue = 0
    for hand in hands:
        red = max(red, hand["red"])
        blue = max(blue, hand["blue"])
        green = max(green, hand["green"])

    return red * green * blue

total = 0
total_power = 0

for line in lines:
    row = line.rstrip()

    hands = row.split("; ")

    # first hand also contains game id, so split again
    game_id, hands[0] = hands[0].split(": ")
    _, game_id = game_id.split(" ")

    # create list with dictionories, that contain the number of colors for each hand
    handdicts = []
    for hand in hands:
        handdict = { # make sure all colors exist, by starting at 0
            "green": 0,
            "red": 0,
            "blue": 0
        }
        for colors in hand.split(", "):
            n, color = colors.split(" ")
            handdict[color] = int(n)
        handdicts.append(handdict)

    # only possible hands are added
    if is_possible(handdicts):
        total+= int(game_id)

    # all hands contribute to total power
    total_power += power(handdicts)

print("Part 1, total", total)
print("Part 2, total power", total_power)
