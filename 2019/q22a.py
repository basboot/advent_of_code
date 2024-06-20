# Using readlines()
from networkx import shortest_path

from tools.advent_tools import *

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

deck = list(range(10007))



for line in lines:
    command = line.rstrip()

    if command == "deal into new stack":
        deck.reverse()
    else:
        splitted_command = command.split(" ")
        value = int(splitted_command[-1])
        if splitted_command[0] == "cut":
            deck = deck[value:] + deck[:value]

        if splitted_command[0] == "deal":
            old_deck = deck.copy()
            for i in range(len(deck)):
                deck[(i * value) % len(deck)] = old_deck[i]


print(deck.index(2019))