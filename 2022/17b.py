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
MAX_BLOCKS = 1000000000000 # number of blocks to fall

ENABLE_MODULUS = True # disable for part 1, and drawing
WARM_UP = 2 * len(jet_pattern)  # try to find modulus after WARM_UP blocks

start_modulus_shape = None      # block used to find start of modulus
start_modulus_height = None     # height from which we try to find the modules
skipped_height = 0              # store height skipped after we find modulus and reduce MAX_BLOCKS

sequence = []

while n_blocks < MAX_BLOCKS:
    # create new block if last block was stuck
    if block_fixed:
        falling_block = create_block(next_shape, highest_fixed_pixel + 4)
        block_fixed = False

        if falling_block is not None:
            show_world(7, highest_fixed_pixel + 10, falling_block, "NEW BLOCK")

    if n_blocks == WARM_UP and start_modulus_shape is None:
        print("WARM UP over")
        start_modulus_shape = next_shape
        start_modulus_height = highest_fixed_pixel

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
        # find repeating sequence by combining block id and x pos of first pixel
        x_block = falling_block[0][0]
        if start_modulus_shape is not None:
            sequence.append((next_shape, x_block))

        block_fixed = True
        add_block_to_world(falling_block)
        n_blocks += 1
        falling_block = None
        next_shape = (next_shape + 1) % len(blocks) # prepare next block

        if ENABLE_MODULUS and next_shape == start_modulus_shape:
            # new round of blocks, have we found the modulus?

            # only possible for even length
            if len(sequence) % 2 == 0:
                first_half = sequence[0: len(sequence)// 2]
                second_half = sequence[len(sequence) // 2:]

                if first_half == second_half:
                    print(f"Modulus found = {len(first_half)}, height of modulus = {(highest_fixed_pixel - start_modulus_height) / 2}")

                    # reduce max blocks
                    modulus = len(first_half)
                    blocks_to_go = MAX_BLOCKS - n_blocks

                    reduced_cycles = blocks_to_go // modulus
                    blocks_left = blocks_to_go % modulus

                    skipped_height = ((highest_fixed_pixel - start_modulus_height) / 2) * reduced_cycles

                    MAX_BLOCKS = blocks_left + n_blocks # add current blocks because we have passed the modulus already


show_world(7, highest_fixed_pixel + 2, [], "END")
print(f"Part 2, highest {int(highest_fixed_pixel + skipped_height)}")



