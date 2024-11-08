file1 = open('q21a.txt', 'r')
file_lines = file1.readlines()

last_dice = -1
def deterministic_dice():
    global last_dice
    last_dice = (last_dice + 1) % 100
    return last_dice + 1

players = []
for line in file_lines:
    players.append(int(line.rstrip().split(" ")[4]) - 1) # 0-9 == 1-10!

print(players)

points = [0] * len(players)

current_player = 0

N_THROWS = 3
MAX_POINTS = 1000
def play_turn(current_player, players, points):
    dice = 0
    for _ in range(N_THROWS):
        dice += deterministic_dice()

    players[current_player] = (players[current_player] + dice) % 10
    points[current_player] += players[current_player] + 1 # + 1 for 1-10

    game_over = points[current_player] >= MAX_POINTS
    current_player = (current_player + 1) % len(players)

    return current_player, players, points, game_over


game_over = False
rolls = 0
while not game_over:
    rolls += N_THROWS
    current_player, players, points, game_over = play_turn(current_player, players, points)
    print(current_player, players, points, rolls)

print("Part 1", points[current_player] * rolls)

