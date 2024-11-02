import math
from collections import Counter, deque
import numpy as np
from scipy.signal import convolve2d

N_PLAYERS = 438 # notice we start at player 0, not 1
LAST_MARBLE = 71626 * 100

scores = [0] * N_PLAYERS

# init circle with first marble
circle = deque([0]) # use deque for fast list mutations
current_player = 0
current_marble = 1


while current_marble < LAST_MARBLE + 1:
    if current_marble % 23 == 0:
        circle.rotate(7) # remove 7 back
        removed_marble = circle.pop()
        circle.rotate(-1) # move to next
        scores[current_player] += (current_marble + removed_marble)
    else:
        circle.rotate(-1) # rotate left, to insert one further
        circle.append(current_marble)

    # print(current_player, circle)
    current_marble += 1
    current_player = (current_player + 1) % N_PLAYERS


print("High score", max(scores))