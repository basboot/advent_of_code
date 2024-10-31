import heapq
import itertools
from collections import defaultdict
from random import random, shuffle

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *
import re

from sympy import divisors


COST, DAMAGE, HEAL, ARMOR, MANA, TIMER = 0, 1, 2, 3, 4, 5

# Magic Missile costs 53 mana. It instantly does 4 damage.
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

EFFECTS = [
    (53, 4, 0, 0, 0, 1),
    (73, 2, 2, 0, 0, 1),
    (113, 0, 0, 7, 0, 6),
    (173, 3, 0, 0, 0, 6),
    (229, 0, 0, 0, 101, 5)
]

def spells(mana, active):
    results = []
    for i in range(len(EFFECTS)):
        if active[i] > 0: # cannot cast spell twice
            continue
        if EFFECTS[i][COST] <= mana:
            results.append(i)
    return results


MANA_SPENT, PLAYER_HP, BOSS_HP, PLAYER_MANA = 0, 1, 2, 3

def fight(player_hp, boss_hp, player_mana, boss_damage):
    start = [0, player_hp, boss_hp, player_mana, [0, 0, 0, 0, 0]]

    explore = []
    heapq.heappush(explore, start)

    while True and len(explore) > 0:
        cost, player_hp, boss_hp, player_mana, active = heapq.heappop(explore)

        if boss_hp <= 0:
            print("WON")
            print(f"Total mana spent {cost}")
            return # won
        
        if player_hp <= 0:
            # print("player dead")
            continue # cannot play anymore


        # TODO: need visited?
        # process effects
        for i in range(len(EFFECTS)):
            if active[i] > 0:
                player_hp += EFFECTS[i][HEAL]
                boss_hp -= EFFECTS[i][DAMAGE]
                player_mana += EFFECTS[i][MANA]
                active[i] -= 1

        effect_ids = spells(player_mana, active)

        if len(effect_ids) == 0: # lose when no spell can be cast
            continue

        for effect_id in effect_ids:
            new_active = active.copy()
            new_active[effect_id] = EFFECTS[effect_id][TIMER]

            new_player_mana = player_mana - EFFECTS[effect_id][COST]
            new_player_hp = player_hp
            new_boss_hp = boss_hp

            # process effects
            new_armor = 0
            for i in range(len(EFFECTS)):
                if new_active[i] > 0:
                    new_player_hp += EFFECTS[i][HEAL]
                    new_boss_hp -= EFFECTS[i][DAMAGE]
                    new_player_mana += EFFECTS[i][MANA]
                    new_armor = EFFECTS[i][ARMOR]
                    new_active[i] -= 1


            # if boss still alive, then fight back
            if new_boss_hp > 0:
                damage = max(1, boss_damage - new_armor)
                new_player_hp -= damage
            else:
                print("boss dead")

            # store state
            state = [cost + EFFECTS[effect_id][COST], new_player_hp, new_boss_hp, new_player_mana, new_active]

            heapq.heappush(explore, state)



# initial
player_hp = 50
player_mana = 500
# Hit Points: 58
# Damage: 9
boss_hp = 58
boss_damage = 9
fight(player_hp, boss_hp, player_mana, boss_damage)

# 226 too low