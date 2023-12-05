# Using readlines()
file1 = open('q17a.txt', 'r')
lines = file1.readlines()

# Each rock appears so that its left edge is two units away from the left wall and its bottom
# edge is three units above the highest rock in the room (or the floor, if there isn't one).

# origin = bottom, left of containing rectangle
# last 'pixel' is highest
# up and right is positive

blocks = [
    (
        (0, 0), (1, 0), (2, 0), (3, 0) # -
    ),
    (
        (1, 0), (0, 1), (1, 1), (2, 1), (1, 2) # +
    ),
    (
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2) # L (reverse)
    ),
    (
        (0, 0), (0, 1), (0, 2), (0, 3) # |
    ),
    (
        (0, 0), (0, 1), (1, 0), (1, 1) # square
    )
]

world = {
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6) # floot
}

current_shape = 0
current_level = 0
block_fixed = True

for line in lines:
    row = line.rstrip()
    print("input: ", row)

def create_block(shape, level):
    block = []
    for pixel in blocks[shape]:
        block.append([pixel[0] + 2, pixel[1] + level])

    return block

def move_block(block, direction):
    # TODO: check if no places are occupied in direction (x, y)
    # True if possible, return new position
    # False if not possible, return old position
    return True, block

falling_block = None

for i in range(10):
    # create new block if last block was stuck
    if block_fixed:
        falling_block = create_block(current_shape, current_level)
        current_shape = (current_shape + 1) % len(blocks) # prepare next block

    # jets # TODO: get direction from input
    _, falling_block = move_block(falling_block, (0, 0))

    # gravity
    not_stuck, falling_block = move_block(falling_block, (0, -1))

    if not not_stuck:
        block_fixed = True
        current_level = falling_block[-1][1] # y pos of last pixel

        # add pixels to world




