import numpy as np

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

players = []
player = []

for i in range(1, len(lines)):
    line = lines[i].rstrip()

    if line.isnumeric():
        player.append(int(line))
    else:
        if len(player) > 0:
            players.append(player)
            player = []

players.append(player) # last player

# def play_normal_combat(players): # mutable!
#     card1 = players[0].pop(0)
#     card2 = players[1].pop(0)
#
#     if card1 > card2:
#         players[0] += [card1, card2]
#     else:
#         players[1] += [card2, card1]
#
#     return players


def is_round_recurring(players, previous_rounds):
    round = (tuple(players[0]), tuple(players[1]))

    if round in previous_rounds:
        return True # already played
    else:
        # new, so add to history
        previous_rounds.add(round)
        return False

#while True: # play until win

def normal_game(card1, card2):
    if card1 > card2:
        return 0
    else:
        return 1

def play_round(players, previous_rounds):
    winner = 0
    game_over = True
    print(players)

    # player 0 wins, game over if hand already occured
    if not is_round_recurring(players, previous_rounds):

        if len(players[0]) == 0:
            return 1, True

        if len(players[1]) == 0:
            return 0, True

        game_over = False

        card1 = players[0].pop(0)
        card2 = players[1].pop(0)

        if card1 > len(players[0]) or card2 > len(players[1]):
            # not enough cards for recursive, highest card wins
            winner = normal_game(card1, card2)
        else:
            # recurse
            print("recurse")
            winner = play_game([players[0][0:card1], players[1][0:card2]])
            print(f"winner = {winner}")
            print("end recurse")

        players[winner] += [card1, card2] if winner == 0 else [card2, card1]
    else:
        print("recurring round")

    return winner, game_over

def play_game(players):
    game_over = False
    previous_rounds = set()
    winner = 0
    while not game_over:
        winner, game_over = play_round(players, previous_rounds)
    return winner

winner = play_game(players)

winning = players[winner]

winning.reverse()

total = 0
for i in range(len(winning)):
    total += ((i + 1) * winning[i])

print(total)


# [[8], [10, 9, 7, 5]]
# end recurse
# [[8, 3, 1, 4], [10, 9, 7, 5, 6, 2]] FOUT, ANDERE SPELER WINT