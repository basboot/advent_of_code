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

highest_fixed_pixel = 0

world = {
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0) # floot
}

DEBUG = True

# show fixed blocks and not fixed 'block' passed as parameter for debugging
def show_world(w, h, block, message, debug=DEBUG):
    if DEBUG:
        return
    # create copy of world
    world_copy = world.copy()

    # add block to copy of world
    for pixel in block:
        # print(f"add {pixel}")
        world_copy.add(tuple(pixel))

    print(f"---------{message}-----------")

    # show copy of world
    for y in range(h, 0, -1):
        for x in range(w):
            if (x, y) in world_copy:
                print("#", end="")
            else:
                print(".", end="")
        print()

# wind blowing pattern
jet_pattern = lines[0].rstrip()

# create block = array of pixels, starting at height 'level', 2 from the wall
def create_block(shape, level):
    block = []
    for pixel in blocks[shape]:
        block.append([pixel[0] + 2, pixel[1] + level])

    return block

# move block and return True, moved_block or False, not_moved_block if it is stuck
def move_block(block, direction):
    # True if possible, return new position
    # False if not possible, return old position
    dx, dy = direction

    # check move is possible in world
    for pixel in block:
        if (pixel[0] + dx, pixel[1] + dy) in world or pixel[0] + dx < 0 or pixel[0] + dx > 6:
            return False, block
    # do move
    for pixel in block:
        pixel[0] += dx
        pixel[1] += dy

    return True, block


def add_block_to_world(block):
    global world
    global highest_fixed_pixel

    for pixel in block:
        world.add((pixel[0], pixel[1]))
        highest_fixed_pixel = max(highest_fixed_pixel, pixel[1])

next_shape = 0 # next block to pick
block_fixed = True # current block cannot move
falling_block = None # current block
jet_i = 0

n_blocks = 0
MAX_BLOCKS = 2022

while n_blocks < MAX_BLOCKS:
    # create new block if last block was stuck
    if block_fixed:
        falling_block = create_block(next_shape, highest_fixed_pixel + 4)
        block_fixed = False

        if falling_block is not None:
            show_world(7, highest_fixed_pixel + 10, falling_block, "NEW BLOCK")


    # jets
    direction = (-1, 0) if jet_pattern[jet_i % len(jet_pattern)] == "<" else (+1, 0)
    _, falling_block = move_block(falling_block, direction)

    if falling_block is not None:
        show_world(7, highest_fixed_pixel + 10, falling_block, f"PUSHED {jet_pattern[jet_i % len(jet_pattern)]}")

    jet_i += 1

    # gravity
    not_stuck, falling_block = move_block(falling_block, (0, -1))
    if falling_block is not None:
        show_world(7, highest_fixed_pixel + 10, falling_block, "FALLEN")

    if not not_stuck:
        block_fixed = True
        add_block_to_world(falling_block)
        n_blocks += 1
        falling_block = None


show_world(7, highest_fixed_pixel + 2, [], "END")
print(f"Part 2, highest {int(highest_fixed_pixel)}")



