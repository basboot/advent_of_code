# Using readlines()
import math

file1 = open('q12a.txt', 'r')
lines = file1.readlines()

def actions(position):
    result = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            # print("check", position[0] + i, position[1] + j)
            # skip current
            if i == 0 and j == 0:
                # print("equal")
                continue
            # skip outside map
            # skip diagonals
            if abs(i) + abs(j) > 1:
                # print("diagonal")
                continue
            if (position[0] + i < 0 or position[1] + j < 0 or
                    position[0] + i > len(map) - 1 or position[1] + j > len(map[0]) - 1):
                # print("outside")
                continue
            # skip places too high
            if map[position[0] + i][position[1] + j] > map[position[0]][position[1]] + 1:
                # print("too high")
                continue
            # add action
            result.append((position[0] + i, position[1] + j))
    return result

# def bfs(position, explored, route):
#     # print(position, route)
#     if position == goal:
#         print(f"Reached goal with route length {len(route)} ({route})")
#
#     # stop path when already explored
#     if position in explored:
#         return
#     # avoid exploring again
#     explored.add(position)
#
#     for next_position in actions(position):
#         bfs(next_position, explored.copy(), route + [next_position])


import collections

# BFS algorithm
def bfs(root):

    route_len = None
    visited, queue = set(), collections.deque([(root, [root])])
    visited.add(root)

    while queue:

        # Dequeue a vertex from queue
        vertex, route = queue.popleft()

        if vertex == goal:
            # print(f"found route steps {len(route) - 1} ({route})")
            route_len = len(route) - 1
            break


        # print(str(vertex) + " ", end="")

        # If not visited, mark it as visited, and
        # enqueue it
        for neighbour in actions(vertex):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, route + [neighbour]))

    return route_len

map = []

start = None
goal = None

i = 0
for line in lines:
    row = line.rstrip()
    # print("input: ", row)

    map_row = []
    j = 0
    for c in row:
        match c:
            case "S":
                start = (i, j)
                map_row.append(ord('a') - ord('a'))
            case "E":
                goal = (i, j)
                map_row.append(ord('z') - ord('a'))
            case _:
                map_row.append(ord(c) - ord('a'))

        j += 1
    map.append(map_row)
    i += 1

print(map)
# print(start, goal)
# print(map[2][5]) # i, j
# print(actions((1, 5)))
print(f"Part 1. Shortest route is {bfs(start)}")

shortest = math.inf
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == 0:
            # print(i, j)
            new_route = bfs((i, j))
            if new_route is not None:
                shortest = min(shortest, new_route)


print(f"Part 2. Shortest route is {shortest}")