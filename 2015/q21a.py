import itertools

# shop
# Weapons dictionary
weapons = {
    "Dagger": {"Cost": 8, "Damage": 4, "Armor": 0},
    "Shortsword": {"Cost": 10, "Damage": 5, "Armor": 0},
    "Warhammer": {"Cost": 25, "Damage": 6, "Armor": 0},
    "Longsword": {"Cost": 40, "Damage": 7, "Armor": 0},
    "Greataxe": {"Cost": 74, "Damage": 8, "Armor": 0},
}

# Armor dictionary
armors = {
    "Leather": {"Cost": 13, "Damage": 0, "Armor": 1},
    "Chainmail": {"Cost": 31, "Damage": 0, "Armor": 2},
    "Splintmail": {"Cost": 53, "Damage": 0, "Armor": 3},
    "Bandedmail": {"Cost": 75, "Damage": 0, "Armor": 4},
    "Platemail": {"Cost": 102, "Damage": 0, "Armor": 5},
    "None": {"Cost": 0, "Damage": 0, "Armor": 0},
}

# Rings dictionary
rings = {
    "Damage +1": {"Cost": 25, "Damage": 1, "Armor": 0},
    "Damage +2": {"Cost": 50, "Damage": 2, "Armor": 0},
    "Damage +3": {"Cost": 100, "Damage": 3, "Armor": 0},
    "Defense +1": {"Cost": 20, "Damage": 0, "Armor": 1},
    "Defense +2": {"Cost": 40, "Damage": 0, "Armor": 2},
    "Defense +3": {"Cost": 80, "Damage": 0, "Armor": 3},
    "None1": {"Cost": 0, "Damage": 0, "Armor": 0},
    "None2": {"Cost": 0, "Damage": 0, "Armor": 0},
}

def config(items):
    cost = damage = armor = 0
    for item in items:
        cost += item["Cost"]
        damage += item["Damage"]
        armor += item["Armor"]

    return cost, damage, armor

class Player():
    def __init__(self, c, hp):
        self.cost = c[0]
        self.damage = c[1]
        self.armor = c[2]
        self.hp = hp

    def __str__(self):
        return f"health {self.hp}"

def attack(player1: Player, player2: Player):
    # player 1 attacks
    damage = max(1, player1.damage - player2.armor)
    player2.hp -= damage

def fight(players: list[Player]):
    turn = 0
    while players[0].hp > 0 and players[1].hp > 0:
        attack(players[(0 + turn) % 2], players[(1 + turn) % 2])
        turn += 1

    print(players[0])
    return 0 if players[0].hp > 0 else 1


results = []
losses = []

# armor and rings have none-type, so we can always fully equip
for weapon in weapons.values():
    for armor in armors.values():
        for ring in itertools.combinations(rings.values(), 2):

            # Hit Points: 104
            # Damage: 8
            # Armor: 1
            boss = Player((0, 8, 1), 104)
            me = Player(config([weapon, armor] + list(ring)), 100)

            if (fight([me, boss])) == 0: # win
                results.append(me.cost)
            else:
                losses.append(me.cost)


results.sort()
print("Part 1", results[0])

losses.sort(reverse=True)
print("Part 2", losses[0])

