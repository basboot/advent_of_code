import heapq
import itertools
from collections import defaultdict
from copy import copy
from functools import total_ordering
from random import random, shuffle

import numpy as np
from mip import maximize
from numpy.core.defchararray import isnumeric
from mip import *
import re

from sympy import divisors


from dataclasses import dataclass

@total_ordering
@dataclass
class GameState:
    """Class for keeping track of the gamestate."""
    player_hp: int
    player_mana: int
    player_armor: int
    boss_hp: int
    boss_damage: int

    total_cost: int
    effect_timer:list

    def active(self, i):
        return self.effect_timer[i] > 0

    def activate(self, i, t):
        self.effect_timer[i] = t

    def __post_init__(self):
        self.sort_index = self.total_cost

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __copy__(self):
        return GameState(self.player_hp, self.player_mana, self.player_armor, self.boss_hp, self.boss_damage, self.total_cost, self.effect_timer.copy())

@dataclass
class Effect:
    cost: int
    damage: int
    heal: int
    armor: int
    mana: int
    time: int

effects = [
    Effect(53, 4, 0, 0, 0, 1),
    Effect(73, 2, 2, 0, 0, 1),
    Effect(113, 0, 0, 7, 0, 6),
    Effect(173, 3, 0, 0, 0, 6),
    Effect(229, 0, 0, 0, 101, 5)
]


def perform_effects(gamestate: GameState):
    next_gamestate = copy(gamestate)
    next_gamestate.player_armor = 0 # reset armor, before effects

    for i in range(len(effects)):
        if next_gamestate.active(i):
            next_gamestate.boss_hp -= effects[i].damage
            next_gamestate.player_hp += effects[i].heal
            next_gamestate.player_armor += effects[i].armor
            next_gamestate.player_mana += effects[i].mana
            next_gamestate.effect_timer[i] -= 1

    return next_gamestate

def perform_boss_attack(gamestate: GameState):
    next_gamestate = copy(gamestate)
    if next_gamestate.boss_hp > 0: # only alive bosses can fight
        damage = max(1, next_gamestate.boss_damage - next_gamestate.player_armor)
        next_gamestate.player_hp -= damage
    return next_gamestate

def possible_effects(gamestate):
    results = []
    for i in range(len(effects)):
        if gamestate.active(i): # cannot cast spell twice
            continue
        if effects[i].cost <= gamestate.player_mana:
            results.append(i)
    return results


def fight(gamestate):
    explore: list[GameState] = []
    heapq.heappush(explore, gamestate)

    while True and len(explore) > 0:
        gamestate = heapq.heappop(explore)

        # Part 2
        # At the start of each player turn (before any other effects apply)
        gamestate.player_hp -= 1

        # check lose (no need to search further)
        if gamestate.player_hp <= 0:
            continue

        # effects before
        gamestate = perform_effects(gamestate)

        # check win (found best result) after effects (if boss was dead he will still be)
        if gamestate.boss_hp <= 0:
            print("FOUND")
            print("Mana spent", gamestate.total_cost)
            break

        possible_effect_ids = possible_effects(gamestate)

        if len(possible_effect_ids) == 0:  # lose when no spell can be cast
            continue

        for possible_effect_id in possible_effect_ids:
            next_gamestate = copy(gamestate)
            # apply effect
            next_gamestate.activate(possible_effect_id, effects[possible_effect_id].time)
            next_gamestate.player_mana -= effects[possible_effect_id].cost
            next_gamestate.total_cost += effects[possible_effect_id].cost

            # effects after
            next_gamestate = perform_effects(next_gamestate)

            # boss fights back (if not dead)
            next_gamestate = perform_boss_attack(next_gamestate)

            # store state
            heapq.heappush(explore, next_gamestate)


gamestate = GameState(50, 500, 0, 58, 9, 0, [0] * len(effects))

# For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:
# gamestate = GameState(10, 250, 0, 13, 8, 0, [0] * len(effects))

fight(gamestate)
