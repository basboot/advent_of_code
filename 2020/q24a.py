file1 = open('q24a.txt', 'r')
lines = file1.readlines()

instructions = [x.rstrip() for x in lines]

# print(instructions)

directions = {
    "e": (0, 2),
    "se": (1, 1),
    "sw": (1, -1),
    "w": (0, -2),
    "nw": (-1, -1),
    "ne": (-1, 1)
}

def follow_instruction(instruction):
    i, j = 0, 0
    while len(instruction) > 0:
        for direction in directions:
            if instruction.startswith(direction):
                di, dj = directions[direction]
                i += di
                j += dj
                instruction = instruction[len(direction):] # cut off direction
                break
    return i, j

black_tiles = set()

for instruction in instructions:
    position = follow_instruction(instruction)
    if position in black_tiles:
        black_tiles.remove(position)
    else:
        black_tiles.add(position)

print("Part 1", len(black_tiles))

#

for i in range(100):
    neighbours = {}
    for black_tile in black_tiles:
        for direction in directions:
            i, j = black_tile
            di, dj = directions[direction]
            neighbour = (i + di, j + dj)
            if neighbour in neighbours:
                neighbours[neighbour] += 1
            else:
                neighbours[neighbour] = 1

    new_black_tiles = set()
    # first handle black tiles
    for black_tile in black_tiles:
        if black_tile in neighbours:
            pass
            if neighbours[black_tile] < 3: # more than two neighbours becomes white, else it stays black
                new_black_tiles.add(black_tile)
        else:
            # zero neighbours, remove
            pass

    # handle white tiles
    for neighbour in neighbours:
        if neighbour in black_tiles:
            continue # black tiles already processed
        if neighbours[neighbour] == 2: # exactly 2 neighbours becomes black
            new_black_tiles.add(neighbour)

    black_tiles = new_black_tiles
    # print(black_tiles)

print("Part 2", len(black_tiles))
