# Using readlines()
file1 = open('q4a.txt', 'r')
lines = file1.readlines()

score = 0

scratchcards = []
for line in lines:
    current_score = 0
    row = line.rstrip()
    card_number, card_info = row.replace("  "," ").replace("  "," ").replace("  "," ").replace("Card ", "").split(": ")
    winning_numbers_str, current_numbers_str = card_info.split(" | ")

    winning_numbers = [int(x) for x in winning_numbers_str.split(" ")]
    current_numbers = set([int(x) for x in current_numbers_str.split(" ")])

    # store cards in array for part 2
    scratchcards.append({
        "winning_numbers" : winning_numbers,
        "current_numbers": current_numbers,
        "instances": 1 # number of instances of this card
    })

    # check winning numbers, calculate score annd add score to total
    for n in current_numbers:
        if n in winning_numbers:
            if current_score == 0:
                current_score = 1
            else:
                current_score *= 2

    score += current_score

print("Part 1", score)

# Part 2: wining cards give extra instances of the next cards
for i in range(len(scratchcards)):

    # count winning numbers on this card
    current_score = 0
    for n in scratchcards[i]["current_numbers"]:
        if n in scratchcards[i]["winning_numbers"]:
            current_score += 1

    # use score to increase next #score cards, by the # of instances of this card
    for j in range(current_score):
        if i + j + 1 < len(scratchcards): # never win beyond end
            scratchcards[i + j + 1]["instances"] += scratchcards[i]["instances"]

# count total card instances
total = 0
for scratchcard in scratchcards:
    total += scratchcard["instances"]

print("Part 2", total)









