from tools.advent_tools import *

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

tiles = {}
new_tile = True
tile_id = -1
tile = []
tile_size = 10 # TODO; dynamic?

def create_orientations(tile):
    # tuple(map(tuple, arr))
    options = ([np.rot90(np.array(tile), k) for k in range(4)]
               + [np.rot90(np.flip(np.array(tile), 0), k) for k in range(4)])

    used = set()
    unique = []
    for option in options:
        t_array = tuple(map(tuple, option))
        if t_array not in used:
            used.add(t_array)
            unique.append(option)
    return (unique)

for i in range(len(lines)):
    line = lines[i].rstrip()

    # Tile 2311:
    if new_tile:
        tile_id = int(line.replace(":", "").split(" ")[1])
        new_tile = False
        continue

    if line == "":
        tiles[tile_id] = create_orientations(tile)
        new_tile = True
        tile = []
        continue

    tile.append([int(x) for x in line.replace(".", "0").replace("#", "1")])

    if line == "":
        read_rules = False
        continue


tiles[tile_id] = create_orientations(tile)

#
n_tiles = 0
for tile in tiles:
    n_tiles += len(tiles[tile])
print("# tiles", n_tiles) # 1728 => 1152 na check uniqueness (was error => flip x + rotate == flip y + rotate)

print(len(tiles), math.sqrt(len(tiles)))

puzzle_size = int(math.sqrt(len(tiles)))

def tile_fits(solution, tile, position):
    # check all four sides for match
    i, j = position

    # above
    if (i - 1, j) in solution: # only check if adjacent tile in solution
        if not np.array_equal(solution[(i - 1, j)][tile_size - 1, :], tile[0, :]):
            return False # no match
    # below
    if (i + 1, j) in solution: # only check if adjacent tile in solution
        if not np.array_equal(solution[(i + 1, j)][0, :], tile[tile_size - 1, :]):
            return False # no match
    # left
    if (i, j - 1) in solution: # only check if adjacent tile in solution
        if not np.array_equal(solution[(i, j - 1)][:, tile_size - 1], tile[:, 0]):
            return False # no match

    # right
    if (i, j + 1) in solution: # only check if adjacent tile in solution
        if not np.array_equal(solution[(i, j + 1)][:, 0], tile[:, tile_size - 1]):
            return False # no match

    return True


def solve_puzzle(position, tiles, used, solution, ids):
    # update position
    i, j = position
    j += 1
    if j == puzzle_size:
        j = 0
        i += 1

    # check if done (all pieces placed)
    if i == puzzle_size:
        return solution, ids

    # try all unused pieces
    for tile in tiles:
        if tile in used:
            continue
        # try all orientations
        for orientation in range(len(tiles[tile])):
            if tile_fits(solution, tiles[tile][orientation], (i, j)):
                # fits, update solution and try next
                solution[(i, j)] = tiles[tile][orientation]
                used.add(tile)
                ids[(i, j)] = tile
                p_solution, p_ids = solve_puzzle((i, j), tiles, used, solution, ids)
                if p_solution is not None:
                    return p_solution, p_ids
                # if None returns it did not work, so backtrack
                del solution[(i, j)]
                del ids[(i, j)]
                used.remove(tile)
    return None, None


solution, ids = solve_puzzle((0, -1), tiles, set(), {}, {})

print("Part 1", ids[(0, 0)] * ids[(0, puzzle_size - 1)] * ids[(puzzle_size - 1, 0)] * ids[(puzzle_size - 1, puzzle_size - 1)])

file2 = open('q20b.txt', 'r')
lines = file2.readlines()
sea_monster, s_width, s_height = read_grid(lines, GRID_NUMPY, f_prepare_line=lambda x: x.rstrip(), value_conversions={"#": 1, ".": 0})
# print(sea_monster)

# create full puzzle by combining the pieces
piece_size = tile_size - 2
puzzle = np.zeros((puzzle_size * piece_size, puzzle_size * piece_size), dtype=int)
for i in range(puzzle_size):
    for j in range(puzzle_size):
        # remove borders
        piece = solution[(i, j)][1:tile_size - 1, 1:tile_size - 1]
        # put in the puzzle
        puzzle[i * piece_size:(i + 1) * piece_size, j * piece_size:(j + 1) * piece_size] = piece

# scan puzzle for seamonster
count_monsters = 0

# create all possible rotations
rotated_puzzles = ([np.rot90(np.array(puzzle), k) for k in range(4)]
               + [np.rot90(np.flip(np.array(puzzle), 0), k) for k in range(4)])

k = 0 # check puzzle orientations, until a seamonster is found in one
while count_monsters == 0:
    puzzle = rotated_puzzles[k]
    for i in range(puzzle_size * piece_size - s_height + 1):
        for j in range(puzzle_size * piece_size - s_width + 1):
            scan = puzzle[i:i + s_height, j:j + s_width]
            if not np.any((scan - sea_monster) < 0):
                count_monsters += 1
    # print(count_monsters)
    k += 1

# all # in puzzle - # in seamonsters
print("Part 2", np.sum(puzzle) - count_monsters * np.sum(sea_monster))

