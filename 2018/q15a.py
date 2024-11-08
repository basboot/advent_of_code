from functools import cache

file1 = open('q15a.txt', 'r')

# chat gpt
import heapq
from collections import defaultdict

walls = set()

@cache
# cannot cache, because units act like walls
def a_star(start, goal, unit_positions):
    """
    A* algorithm to find all shortest paths between start and goal.

    :param start: Tuple (i, j) representing the starting point.
    :param goal: Tuple (i, j) representing the goal point.
    :param walls: Set of tuples (i, j) representing walls.
    :return: List of all shortest paths from start to goal.
    """

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(node):
        (x, y) = node
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in candidates if (nx, ny) not in walls and (nx, ny) not in units]

    # Priority queue for the A* algorithm
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))

    # Data structures to store the path and costs
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    paths = []

    while open_set:
        _, current_cost, current, path = heapq.heappop(open_set)

        if current == goal:
            paths.append((len(path) - 1, path[1:]))  # remove first step
            continue

        for neighbor in neighbors(current):
            tentative_g_score = current_cost + 1

            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (
                    tentative_g_score + heuristic(neighbor, goal), tentative_g_score, neighbor, path + [neighbor]))
            elif tentative_g_score == g_score[neighbor]:
                heapq.heappush(open_set, (
                    tentative_g_score + heuristic(neighbor, goal), tentative_g_score, neighbor, path + [neighbor]))

    return paths


units = {}

for i, line in enumerate(file1):
    for j, cell in enumerate(line.rstrip()):

        match cell:
            case ".":
                pass
            case "#":
                walls.add((i, j))
            case "G" | "E":
                # sort keys to get correct order
                units[(i, j)] = [200, 3, cell]


def find_units(unit_type):
    units_found = {}
    for pos in units:
        if units[pos][0] < 1:
            continue # prevent adding dead enemies
        if units[pos][2] == unit_type:
            units_found[pos] = units[pos]
    return units_found


def find_adjacent_squares(enemy_units):
    adjacent_squares = set()

    for i, j in enemy_units:
        for di, dj in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            pos = (i + di, j + dj)
            if pos not in walls:
                adjacent_squares.add(pos)

    return adjacent_squares


def show_map(max_size):
    for i in range(max_size):
        summary = "   "
        for j in range(max_size):
            if (i, j) in walls:
                print("#", end="")
                continue
            if (i, j) in units:
                summary += f"{units[(i, j)][2]}({units[(i, j)][0]}), "
                print(units[(i, j)][2], end="")
                continue
            print(".", end="")
        print(summary)

iteration = 0
while True:
    # start turn, sort units
    unit_positions = list(units.keys())
    unit_positions.sort()

    print(f"ITERATION {iteration}")
    show_map(7)

    for pos in unit_positions:
        print("Process unit at", pos)

        if pos not in units:
            continue # dead enemies can be removed during round
        else:
            print("type", units[pos][2])

        # find enemies
        enemies = find_units("G" if units[pos][2] == "E" else "E")
        adjacent_squares = find_adjacent_squares(enemies) # TODO: avoid multiple units in same position (is this needed? we do not move if we don';t have to and move always towards closest)

        print("All attacking adjacent positions: #", len(adjacent_squares))

        if len(adjacent_squares) == 0:
            print("Cannot attack anymore GAME OVER")
            print("Full rounds", iteration)
            print(units)
            total_hp = sum([hp for hp, _, _ in units.values()])
            print("Part 1", total_hp, iteration, iteration * total_hp)
            exit()

        possible_routes = []

        for adjacent_square in adjacent_squares:
            possible_routes += a_star(pos, adjacent_square, tuple(units))

        # put in distamce/reading order
        possible_routes.sort()

        if len(possible_routes) == 0:
            steps = 0
        else:
            steps, route = possible_routes[0]


        # take one step towards closest adjacent square (reading order breaks ties), if needed
        if steps > 0:
            print(steps, route)
            unit = units[pos] # store
            del units[pos] # remove
            assert route[0] not in units, "move on top of other player"
            units[route[0]] = unit # move
            pos = route[0] # set new pos

        # search possible nearby enemies
        i, j = pos
        # can only attack four adjacent squares
        possible_attack_positions = set([(i + di, j + dj) for di, dj in [[-1, 0], [0, 1], [1, 0], [0, -1]]])
        # and if an enemy is on that square
        possible_attack_positions = possible_attack_positions.intersection(set(enemies))

        # is attack possible?
        if len(possible_attack_positions) > 0:
            # create list with HP, pos and unit itself
            possible_attacks = [(units[enemy_pos][0], enemy_pos, units[enemy_pos]) for enemy_pos in possible_attack_positions]
            # sort to get weakest on top, ties broken in reading order
            possible_attacks.sort()
            _, pos_to_attack, unit_to_attack = possible_attacks[0]

            print("attack", unit_to_attack)
            unit_to_attack[0] -= units[pos][1] # remove this unit's AP from other unit's HP

            if unit_to_attack[0] < 1:
                del units[pos_to_attack]  # remove dead enemy

    iteration += 1





# TODO: replace astar with breadth first, to create a lookup table for all locations



