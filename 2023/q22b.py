# Using readlines()
from copy import deepcopy

from tools.advent_tools import *

file1 = open('q22a.txt', 'r')
lines = file1.readlines()

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return np.array([0, 0, 1]) # avoid zero, return unit vector in z direction
    return (v / norm).astype(int)

import numpy as np

bricks = []

world = set()

for line in lines:
    start, end = line.rstrip().split("~")
    start, end = np.array([int(x) for x in start.split(",")]), np.array([int(x) for x in end.split(",")])


    assert sum(end - start) > -1, "We assume all bricks are ordered left to right"

    blocks = []
    d_block = normalize(end - start)


    min_z = math.inf
    max_z = -math.inf

    while sum(end - start) >= 0:
        blocks.append(start)
        min_z = min(min_z, start[2])
        max_z = max(max_z, start[2])
        start = start + d_block

    # print(np.array(blocks), min_z, max_z)

    bricks.append([min_z, max_z, np.array(blocks)]) # needs to be mutable zo we can shift in place

    world = world.union(set(map(tuple, np.array(blocks))))

print(world)

def fall_brick(falling_brick, detect_only=False):
    global world

    min_z, max_z, blocks = falling_brick

    # remove brick from world
    blocks_set = set(map(tuple, blocks))

    world = world - blocks_set
    new_blocks = blocks.copy() # not sure if copy is needed

    dz = 0

    has_changed = False

    while (min_z - dz) > 1: # this is not efficient for long falls!!!
        new_blocks = new_blocks - np.array([0, 0, 1])
        new_blocks_set = set(map(tuple, new_blocks))
        if len(new_blocks_set.intersection(world)) > 0:
            # if there is an intersection we have to stop
            break
        # no intersection, update and go on
        has_changed = True

        if detect_only:
            # abort, before doing changes
            break

        dz += 1
        blocks = new_blocks

    # put back in world
    blocks_set = set(map(tuple, blocks))
    world = world.union(blocks_set)


    return [min_z - dz, max_z - dz, blocks], has_changed

bricks.sort(key=lambda p: p[0])

# perform changes
for i in range(len(bricks)):
    bricks[i], has_changed = fall_brick(bricks[i])
bricks.sort(key=lambda p: p[0])


total = 0
# find chain reaction options
backup_bricks = deepcopy(bricks)
backup_world = world.copy()
for i in range(len(backup_bricks) - 1, -1, -1): # walk in reverse
    print(i)

    # restore everything
    bricks = deepcopy(backup_bricks)
    world = backup_world.copy()

    # desintegrate candidate
    min_z, max_z, blocks = bricks[i]
    # remove candidate from world
    blocks_set = set(map(tuple, blocks))
    world = world - blocks_set
    # and from list!
    bricks.pop(i)

    affected_blocks = 0
    for j in range(i, len(bricks)): # try to move any bricks above, start at i because the block is ectually removed
        bricks[j], has_changed = fall_brick(bricks[j])
        if has_changed:
            affected_blocks += 1

    total += affected_blocks

    # restore world
    world = world.union(blocks_set)

print(world)
print("Total", total)