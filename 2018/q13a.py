import math
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

file1 = open('q13a.txt', 'r')

lines = file1.readlines()

tracks = {} # pos => value
carts = [] # [pos, direction]

CW, CCW = 1j, -1j

# The + must be solved in the update logic
track_mapping = {
    ('\\', 1): CW,
    ('\\', 1j): CCW,
    ('\\', -1): CW,
    ('\\', -1j): CCW,
    ('/', 1): CCW,
    ('/', 1j): CW,
    ('/', -1): CCW,
    ('/', -1j): CW,
}

cart_mapping = { # map cart chat to track char and direction
    '^': ('|', -1j),
    '>': ('-', 1),
    'v': ('|', 1j),
    '<': ('-', -1)
}

for y, line in enumerate(lines):
    for x, value in enumerate(line.rstrip()):
        if value == " ": # skip spaces
            continue
        if value in cart_mapping:
            track, direction = cart_mapping[value]
            carts.append((x + y*1j, direction, 0, False)) # position, direction, crossing_index, crashed
            tracks[x + y*1j] = track
        else:
            tracks[x + y * 1j] = value

# print(tracks)
# print(carts)


crossing_directions = [CCW, 1, CW]

carts_left = len(carts)

while True:
    carts.sort(key=lambda x: (x[0].imag, x[0].real))
    for i in range(len(carts)):
        # get current position
        position, direction, crossing_index, crashed = carts[i]

        if crashed:
            continue # ignore crashed carts

        # update position
        position += direction

        # check if cart needs to change direction
        if (tracks[position], direction) in track_mapping:
            direction *= track_mapping[(tracks[position], direction)]

        if tracks[position] == '+':
            # print(crossing_index)
            direction *= crossing_directions[crossing_index]
            crossing_index = (crossing_index + 1) % 3

        # update cart
        carts[i] = (position, direction, crossing_index, crashed)

        if carts_left == 1: # found only survivor
            print("Last cart at", carts[i][0])
            exit()

        # TODO: improve collision
        for j in range(len(carts)):
            if carts[j][3]: # ignore crashed carts
                continue
            if i == j:
                continue # no collision with self
            if carts[i][0] == carts[j][0]:
                print("Collision at", carts[j][0])

                carts[i] = (0, 0, 0, True) # remove crashed carts
                carts[j] = (0, 0, 0, True)

                carts_left -= 2

    # print(carts)


# Really liked this one. I solved it with complex numbers, which is a trick I learned from earlier years.
# Instead of storing x and y, store position = x + y * i (written y * 1j in python).
#
# The best part about this is that directions are just one of the numbers +1, +1j, -1, -1j and changing a direction
# is as simple as multiplying it by either +1j (clockwise turn) or -1j (counterclockwise turn).
#
# Note that since the Y axis is flipped (positive = down),
# you flip the imaginary part compared to what you'd do in usual mathematics
# (therefore, multiplying by +1j is CW ⭮, not CCW ⭯).