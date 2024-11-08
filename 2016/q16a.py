from collections import Counter
import hashlib

import numpy as np

disk_size = 35651584 #272

initial_state = np.array([int(x) for x in list("00111101111101000")])

# print(initial_state)

state = initial_state == 1

# print(state)

while len(state) < disk_size:
    a = state
    b = np.flip(state)
    b = ~b
    state = np.concatenate([a, [False], b])
    # print(state)

checksum = state[0:disk_size]
# print(checksum)

while len(checksum) % 2 == 0:
    checksum = ~(checksum[::2] ^ checksum[1::2])
    # print(checksum)

print("".join([str(x) for x in checksum.astype(int)]))

#  1 0 0 0 0 0 1 1 1 1 0 0 1 0 0 0 0 1 1 1
#[ 1 0 0 0 0 0 1 1 1 1 0 0 1 0 0 0 0 1 1 1 1 1 0]