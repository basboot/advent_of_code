file1 = open('q4a.txt', 'r')
lines = file1.readlines()

import numpy as np

result = None

bingo_numbers = [int(x) for x in lines[0].rstrip().split(",")]

bingo_cards = []

for i in range(2, len(lines), 6):
    card = []
    for j in range(5):
        row = lines[i+j].rstrip()
        card_row = [int(row[n: n + 3]) for n in range(0, len(row), 3)]
        card.append(card_row)
    bingo_cards.append(card)

# print(bingo_numbers)

n_cards = len(bingo_cards)
cards_that_won = set()

bingo_cards = np.array(bingo_cards)
# print(bingo_cards)


result = bingo_cards & False

# print(result)


first_winning_card = True

for bingo_number in bingo_numbers:
    print("bingo", bingo_number)
    result = result | (bingo_cards == bingo_number)
    # cards win when 'all' are true in axis 1 or 2 in any of the cards (axis 0)
    axis1 = np.any(np.all(result, axis=1))
    axis2 = np.any(np.all(result, axis=2))

    if axis1 or axis2:
        # winning is the card where axis is true, the card index is de first 'coordinate'
        # score can be calculated using 1-result * card * last number

        # check both axis for winning cards, only look at the new ones
        winning_cards = np.where(np.all(result, axis=1))[0]

        for card in winning_cards:
            if card not in cards_that_won:
                cards_that_won.add(card)
                winning_card = card
                print(card)

        winning_cards = np.where(np.all(result, axis=2))[0]

        for card in winning_cards:
            if card not in cards_that_won:
                winning_card = card
                cards_that_won.add(card)
                print(card)


        if first_winning_card:
            # print(winning_card)
            print("first winning", np.sum(((1-result) * bingo_cards)[winning_card]) * bingo_number)
            first_winning_card = False

        # last winning card
        if len(cards_that_won) == n_cards:
            # print(winning_card)
            print("last winning", np.sum(((1 - result) * bingo_cards)[winning_card]) * bingo_number)
            exit() # last found, game over


