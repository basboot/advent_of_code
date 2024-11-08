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

while len(players[0]) > 0 and len(players[1]) >0:
    card1 = players[0].pop(0)
    card2 = players[1].pop(0)

    if card1 > card2:
        players[0] += [card1, card2]
    else:
        players[1] += [card2, card1]


winning = players[0]
if len(players[0]) == 0:
    winning = players[1]

winning.reverse()

total = 0
for i in range(len(winning)):
    total += ((i + 1) * winning[i])

print(total)


