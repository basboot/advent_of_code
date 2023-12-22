# Using readlines()
import math

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

# for brick in bricks:
#     print(brick)
#     print(brick[2].shape)

def fall_brick(bricks, falling_brick, colliding_index, disintegrated_index=None):
    # if other block is marked for disintegration, just skip it as if it were not there
    if disintegrated_index is not None and disintegrated_index == colliding_index:
        return fall_brick(bricks, falling_brick, colliding_index - 1, disintegrated_index=disintegrated_index)

    # hit the ground
    if colliding_index == -1:
        z_min, z_max, brick = falling_brick
        dz = z_min - 1
        if dz == 0:
            return falling_brick, colliding_index + 1, False # return new index
        else:
            return [z_min - dz, z_max - dz, brick - np.array([0, 0, dz])], colliding_index + 1, True

    # hits other brick?
    z_min, z_max, brick = falling_brick
    z_min_other, z_max_other, brick_other = bricks[colliding_index]

    # there are only cubes, so we only have to check if in de xy plane they collide, and then they will collide
    # at height when z_min (this) equals z_max_other
    xy = brick[:,:2]
    xy_other = brick_other[:,:2]

    # add extra axis (with None), then compare by broadcasting to that axis and check if any comparison was true
    # https://stackoverflow.com/questions/63383479/how-to-find-identical-rows-of-two-arrays-with-different-size
    if (xy[None, :] == xy_other[:, None]).all(-1).any(): # colliding?
        dz = z_min - z_max_other - 1 # fall until one above the collision
        if dz == 0:
            return falling_brick, colliding_index + 1, False
        else:
            return [z_min - dz, z_max - dz, brick - np.array([0, 0, dz])], colliding_index + 1, True
    else:
        # no collision with block below, try next
        return fall_brick(bricks, falling_brick, colliding_index - 1, disintegrated_index=disintegrated_index)



for brick in bricks:
    print("--- ", brick[0:2])
    print(brick[2])

def update_bricks(bricks, no_update=False, disintegrated_index=None):
    has_changed = False
    for i in range(len(bricks)):
        # fall until collliding
        falling_brick = bricks[i]
        fallen_brick, new_index, has_fallen = fall_brick(bricks, falling_brick, i - 1, disintegrated_index)

        if has_fallen: # only need te update if somenthing happened
            has_changed = True

            if no_update:
                return bricks, has_changed

            if new_index == i: # just update, no move in list
                bricks[i] = fallen_brick
            else:
                bricks.pop(i) # only moves lower in te list, so new index does not change after pop
                bricks.insert(new_index, fallen_brick) # TODO: it's might be needed to re-sort and start over
                return bricks, has_changed
    return bricks, has_changed

# let bricks from snapshot fall into place
has_changed = True

print("Update snapshot")
while has_changed:
    # print("Fall bricks")
    bricks.sort(key=lambda p: p[0])
    bricks, has_changed = update_bricks(bricks)

for brick in bricks:
    print("--- ", brick[0:2])
    print(brick[2])

exit()
print("Check disintegration")
total = 0
bricks.sort(key=lambda p: p[0])
for i in range(len(bricks)):
    brick_to_disintegrate = i
    bricks, has_changed = update_bricks(bricks, True, brick_to_disintegrate) # possible enhancement, skip blocks below

    if not has_changed:
        total += 1
print("Total", total)

# 423 too high

# Problem with checking collision in order of lower bound, instead of upper bound












