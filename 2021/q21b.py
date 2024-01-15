import math
import sys
from functools import cache
from itertools import combinations, permutations, product
import numpy as np
from tools.advent_tools import *

file1 = open('q21a.txt', 'r')
file_lines = file1.readlines()

sys.setrecursionlimit(10000)

last_dice = -1
def deterministic_dice():
    global last_dice
    last_dice = (last_dice + 1) % 100
    return last_dice + 1

players = []
for line in file_lines:
    players.append(int(line.rstrip().split(" ")[4]) - 1) # 0-9 == 1-10!

# print(players)

points = [0] * len(players)

current_player = 0

N_THROWS = 3
MAX_POINTS = 1000
def play_turn(current_player, players, points, dice):
    players = list(players)
    points = list(points)

    players[current_player] = (players[current_player] + dice) % 10
    points[current_player] += players[current_player] + 1 # + 1 for 1-10

    game_over = points[current_player] >= MAX_POINTS
    current_player = (current_player + 1) % len(players)

    return current_player, tuple(players), tuple(points), game_over


@cache
def number_of_wins(current_player, players, points):
    # print(points)
    if points[(current_player + 1) % 2] >= 21:
        assert points[current_player] < 21, "Something went wrong"
        return np.array([0 if current_player == 0 else 1, 0 if current_player == 1 else 1])

    wins = np.array([0, 0])
    for p in product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
        dice = sum(p)
        players_list = list(players)
        points_list = list(points)

        players_list[current_player] = (players_list[current_player] + dice) % 10
        points_list[current_player] += players_list[current_player] + 1  # + 1 for 1-10

        wins += number_of_wins((current_player + 1) % 2, tuple(players_list), tuple(points_list))

    return wins

wins = number_of_wins(0, tuple(players), tuple(points))

print("Part 2", max(wins))


