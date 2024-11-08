# Using readlines()
import heapq
import sys

from scipy.spatial.distance import cityblock

from tools.advent_tools import *

sys.setrecursionlimit(10000)

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

map, width, height = read_grid(lines, GRID_DICT, lambda a: a.strip())


WIND_CONVERSION = {
    ">": EAST,
    "<": WEST,
    "^": NORTH,
    "v": SOUTH
}
winds = []
# on update create occupied set
valley = set()

def update_winds(winds):
    occupied = set()
    next_winds = []
    for w in range(len(winds)):
        # get wind props
        i, j, di, dj = winds[w]
        # update position
        ni, nj = i + di, j + dj
        # move to other side when it has reached te end
        if ni == 0:
            ni = height - 2
        if nj == 0:
            nj = width - 2
        if ni == height - 1:
            ni = 1
        if nj == width - 1:
            nj = 1

        # update wind
        next_winds.append((ni, nj, di, dj))
        occupied.add((ni, nj))

    return next_winds, occupied


occupied = set()

# create winds array and
for key, value in map.items():
    print(key, "->", value)
    if value == ".":
        continue
    if value == "#":
        valley.add(key)
        continue

    direction = DIRECTIONS[WIND_CONVERSION[value]]
    winds.append((key[0], key[1], direction[0], direction[1]))

    occupied.add((key[0], key[1]))


print(valley)
print(winds)
print(occupied)
winds_repeat_pattern = np.lcm.reduce([height - 2, width - 2])

wind_patterns = [occupied]

for i in range(winds_repeat_pattern - 1):
    winds, occupied = update_winds(winds)
    wind_patterns.append(occupied)



print("#possible states: ", (height - 2) * (width - 2) * np.lcm.reduce([height - 2, width - 2]) + 2)
# 900002, from which most are illegal!

def draw_valley(pos):
    for i in range(height):
        for j in range(width):
            if pos is not None and pos == (i, j):
                print("E", end="")
                continue
            if (i, j) in valley:
                print("#", end="")
            else:
                wind_shown = False
                for iw, jw, diw, djw in winds:
                    if (i, j) == (iw, jw):
                        print("*", end="")
                        wind_shown = True
                        break
                if not wind_shown:
                    print(" ", end="")
        print()

# close the valley, so we don't have to check the boundaries
valley.add((-1, 1))
valley.add((height, width - 2))

start = (0,1)
goal = (height - 1, width - 2)

shortest_length = math.inf

lookup_table = {

}

def get_next_positions(current_pos, wind_pattern):
    i, j = current_pos
    # find next positions
    next_positions = []
    for direction in DIRECTIONS:
        di, dj = DIRECTIONS[direction]
        ni, nj = i + di, j + dj
        next_pos = (ni, nj)

        if next_pos not in valley and next_pos not in wind_patterns[wind_pattern]:
            next_positions.append(next_pos)

    # we can also wait if there is no wind
    if current_pos not in wind_patterns[wind_pattern]:
        next_positions.append(current_pos)

    return next_positions

# no visited possible i think, but try anyway
def dfs(current_pos, visited, length, route, wind_pattern):
    global shortest_length
    if current_pos == goal:
        print("FOUND", current_pos, len(route), route)
        shortest_length = min(length, shortest_length)
        return length, route  #TODO: denk na

    # we cannot use visited like normal because you need to avoid blizards, with this we force not wandering forever
    if length + cityblock(current_pos, goal) >= shortest_length:
        return math.inf, []

    # visited.add(current_pos)

    next_positions = get_next_positions(current_pos, wind_pattern)
    # try to help by prioritizing actions towards the goal
    next_positions.sort()


    min_steps = math.inf
    min_route = []
    for distance_and_next_position in next_positions:
        dist, next_position = distance_and_next_position
        i, j = next_position

        next_wind_pattern = (wind_pattern + 1) % winds_repeat_pattern # avoid walking in circles

        if (i, j, wind_pattern) in visited:
            continue

        new_route = route.copy()
        new_route.append(next_position)
        new_visited = visited.copy()
        new_visited.add((i, j, wind_pattern))
        steps, other_route = dfs(next_position, new_visited, length + 1, new_route, next_wind_pattern)

        if steps < min_steps:
            min_steps = steps
            min_route = other_route

    return min_steps, min_route

def bfs(start, goal, start_wind_pattern=1):
    explored = set()
    to_explore = []
    heapq.heappush(to_explore, (0, start, start_wind_pattern)) # TODO: or 0?

    while len(to_explore) > 0:
        cost_so_far, pos, wind_pattern = heapq.heappop(to_explore)
        if pos == goal:
            return cost_so_far, wind_pattern

        # TODO: check if visiting needs te be here, or can be moved to creating next states
        next_positions = get_next_positions(pos, wind_pattern)
        for next_position in next_positions:
            i, j = next_position
            next_wind = (wind_pattern + 1) % winds_repeat_pattern
            if (i, j, next_wind) in explored:
                continue # en here before, don't go there again
            heapq.heappush(to_explore, (cost_so_far + 1, next_position, next_wind))
            explored.add((i, j, next_wind))

    print("Not found :-(, explored states: ", len(explored))
    return "Not found"




# steps, route = dfs(start, set(), 0, [start], 1)
# print("dfs", steps, route)

steps, wp = bfs(start, goal)
print("bfs start to goal", steps)
steps2, wp = bfs(goal, start, wp+1) # add one for rest/turn ;-)
print("bfs goal to start", steps2)
steps3, wp = bfs(start, goal, wp+1)
print("bfs start to goal", steps3)

print(steps + steps2 + steps3 + 2)

