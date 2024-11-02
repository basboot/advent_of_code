import math
import sys
from dataclasses import dataclass

import numpy as np
from executing import cache
from fontTools.misc.cython import returns
from scipy.spatial.distance import cityblock

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

BOOST = 82 # Part 2, 82 niet goed?

def get_group_by_id(id):
    for group in groups:
        if group.id == id:
            return group

    assert True, "Group noy found"

@dataclass
class Group:
    id: int
    player_id: int
    n_units: int
    hp: int
    immune: list[str]
    weak: list[str]
    damage: int
    damage_type: str
    initiative: int

    # effective power: the number of units in that group multiplied by their attack damage
    def effective_power(self) -> int:
        return self.n_units * self.damage

    # The attacking group chooses to target the group in the enemy army to which it would deal the most damage
    # (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough
    # units to actually receive all of that damage).
    def possible_damage(self, attacker):
        if self.n_units == 0:
            return 0 # cannot die twice
        if self.player_id == attacker.player_id: # cannot do damage to own party
            return 0
        damage = attacker.effective_power() # base
        if attacker.damage_type in self.weak:
            damage *= 2
        if attacker.damage_type in self.immune:
            damage = 0
        return damage

    def attack(self, attacker):
        unit_damage = self.possible_damage(attacker) // self.hp
        self.n_units = max(self.n_units - unit_damage, 0)

        return unit_damage

    def __repr__(self):
        return f"{self.player_id}-{self.id} contains {self.n_units} units"

groups = []

player = 0
id = 0
for line in lines:
    message = line.rstrip()
    if message in ["Immune System:", "Infection:"]:
        continue
    if message == "":
        player = 1
        continue

    # 4485 units each with 2961 hit points (immune to radiation; weak to fire,
    #  cold) with an attack that does 12 slashing damage at initiative 4
    first_part, message = message.split(" (")
    middle_part, end_part = message.split(") ")

    immune = []
    weak = []

    n_units, _, _, _, hp, _, _ = first_part.split(" ")

    for weak_imm in middle_part.split("; "):
        weak_imm_splitted = weak_imm.replace("to ", "").replace(",", "").split(" ")
        if weak_imm_splitted[0] == "immune":
            immune = weak_imm_splitted[1:]
        else:
            weak = weak_imm_splitted[1:]

    _, _, _, _, _, damage, damage_type, _, _, _, initiative = end_part.split(" ")

    groups.append(
        Group(id, player, int(n_units), int(hp), immune, weak, int(damage) + (BOOST if player == 0 else 0), damage_type, int(initiative))
    )
    id += 1


# print(groups)


while True:
    # for group1 in groups:
    #     for group2 in groups:
    #         if group1.player_id == group2.player_id:
    #             continue
    #         print(f"{group1.id} would deal defending {group2.id} damage {group2.possible_damage(group1)}")

    # exit()

    # target selection phase, each group attempts to choose one target.
    # In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first.
    groups.sort(key=lambda g: (g.effective_power(), g.initiative), reverse=True)
    target_selection_order = [g.id for g in groups]
    # print("target select order", target_selection_order)

    planned_attacks = {}
    under_attack = [] # double bookkeeping
    for target_selector_id in target_selection_order:
        target_selector = get_group_by_id(target_selector_id)
        if target_selector.n_units == 0: # cannot play if you are dead
            continue


        # The attacking group chooses to target the group in the enemy army to which it would deal the most damage
        # (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough
        # units to actually receive all of that damage).
        # If an attacking group is considering two defending groups to which it would deal equal damage,
        # it chooses to target the defending group with the largest effective power; if there is still a tie,
        # it chooses the defending group with the highest initiative.
        groups.sort(key=lambda g: (g.possible_damage(target_selector), g.effective_power(), g.initiative), reverse=True)

        targets = list(filter(lambda g: g.id not in under_attack and g.possible_damage(target_selector) > 0, groups))

        if len(targets) > 0:
            planned_attacks[target_selector_id] = targets[0].id
            under_attack.append(targets[0].id)

    groups.sort(key=lambda g: g.initiative, reverse=True)
    attack_order = [g.id for g in groups]
    # print("attack order", attack_order)

    # print(planned_attacks)

    if len(planned_attacks) == 0:
        break # stop when there are no more attacks

    for attacker_id in attack_order:
        if attacker_id not in planned_attacks:
            continue # cannot attack if you have not selected

        attacker = get_group_by_id(attacker_id)
        if attacker.n_units == 0: # cannot play if you are dead
            continue

        attacked = get_group_by_id(planned_attacks[attacker_id])
        # print(attacker_id, "attacks", planned_attacks[attacker_id], "killing units: ", attacked.attack(attacker))

        attacked.attack(attacker)


    groups.sort(key=lambda g: g.id)
    # print(groups)




# print(attack_order)
#
print(groups)

# Immune System:
# Group 2 contains 905 units
# Infection:
# Group 1 contains 797 units
# Group 2 contains 4434 units


units = [0, 0]
for group in groups:
    units[group.player_id] += group.n_units

print("Part 1", units)