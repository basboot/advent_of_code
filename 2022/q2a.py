# Using readlines()
file1 = open('q2a.txt', 'r')
lines = file1.readlines()

# shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the
# outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

# rock, paper, scissors
points_shape = {
    'X' : 1,
    'Y' : 2,
    'Z' : 3,
    'A': 1,
    'B': 2,
    'C': 3
}

player_to_opponent = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

# points for player 1
def rps(player1, player2):
    if player1 == player2: # a-a, b-b, c-c
        return 3
    # r-s
    if player1 == 'A' and player2 == 'C':
        return 6
    # p-r
    if player1 == 'B' and player2 == 'A':
        return 6
    # s-p
    if player1 == 'C' and player2 == 'B':
        return 6

    # lost
    return 0

winning = {
    'A': 'C',
    'B': 'A',
    'C': 'B'
}

losing = {
    'C': 'A',
    'A': 'B',
    'B': 'C'
}

def follow_strategy(player, strategy):
    # X means you need to lose, Y means you need to end the round in a
    # draw, and Z means you need to win.
    if strategy == 'Y':
        return player

    if strategy == 'X':
        return winning[player]

    return losing[player]



total = 0
for line in lines:
    opponent, player = line.strip().split(' ')

    print(opponent, player_to_opponent[player])

    print(rps(player_to_opponent[player], opponent))

    # # 2q
    # playing = player_to_opponent[player]

    #2b
    playing = follow_strategy(opponent, player)

    total += rps(playing, opponent)
    total += points_shape[playing]

print(total)


