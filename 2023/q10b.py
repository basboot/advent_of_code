# Using readlines()
import math
import random

import numpy as np

file1 = open('q10a.txt', 'r')
lines = file1.readlines()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

wind_names=["NORTH", "EAST", "SOUTH", "WEST"]

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this

# add both directions to pipes, for easy navigation
PIPES = {
    "|": {
        NORTH: SOUTH, SOUTH: NORTH
    },
    "-": {
        EAST: WEST, WEST: EAST
    },
    "L": {
        NORTH: EAST, EAST: NORTH
    },
    "J": {
        NORTH: WEST, WEST: NORTH
    },
    "7": {
        SOUTH: WEST, WEST: SOUTH
    },
    "F": {
        SOUTH: EAST, EAST: SOUTH
    },
    ".": None,
        # Empty. No connections
    "S": None
        # Empty, connections unknown, but can be made after we know the map
}

INVERT_DIRECTION = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST
}

# row, col format!
DIRECTIONS = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}

start = None

def calculate_position(position, direction):
    i = position[0] + DIRECTIONS[direction][0]
    j = position[1] + DIRECTIONS[direction][1]

    if 0 <= i < len(maze) and 0 <= j < len(maze[0]):
        return i, j
    else:
        return None

# derive pipe connections from surrounding piped
def derive_connections(this_pipe_position):
    connections = []
    for direction in [NORTH, EAST, SOUTH, WEST]:
        other_pipe_position = calculate_position(this_pipe_position, direction)

        # skip if there is no pipe in this direction
        if other_pipe_position == None:
            continue

        other_pipe = PIPES[maze[other_pipe_position[0]][other_pipe_position[1]]]
        # skip other pipe has no connections
        if other_pipe is None:
            continue

        # check if other pipe has a connection towards this pip
        if INVERT_DIRECTION[direction] in other_pipe:
            connections.append(direction)

    assert len(connections) == 2, "pipes always have exactly 2 connections"

    return {
        connections[0]: connections[1], connections[1]: connections[0]
    }


# -1 left, 1 right, 0 straight
def left_or_right(direction1, direction2):
    return np.sign(direction1[0] * direction2[1] - direction1[1] * direction2[0])

def show_maze(maze, marked=set()):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in marked:
                print("X", end="")
            else:
                print(maze[i][j], end="")
        print()

# recursively mark position and neighbours
def mark_tiles(position):
    if position in marked:
        return
    marked.add(position)
    for direction in [NORTH, EAST, SOUTH, WEST]:
        next_position = calculate_position(position, direction)
        if next_position is not None and next_position not in marked:
            mark_tiles(next_position)

maze = []
for i in range(len(lines)):
    row = list(lines[i].rstrip())

    for j in range(len(row)):
        if row[j] == "S":
            start = (i, j)
    maze.append(row)

assert start is not None, "S not found"

# derive S config from pipes around it
PIPES["S"] = derive_connections(start)

# walk through the pipes, start at S
current_position = start # S
# next_direction = next(iter(PIPES["S"])) # just get first direction from S

start_from_direction, start_next_direction = random.choice(list(PIPES["S"].items()))
previous_direction, next_direction = start_from_direction, start_next_direction

route_len = 0
turns = 0

marked = set() # mark every visited tile (to mark boundaries)

while True:
    route_len += 1
    # count left/right turns to know what is te inside of the route
    turns += left_or_right(DIRECTIONS[INVERT_DIRECTION[previous_direction]], DIRECTIONS[next_direction])
    marked.add(current_position)

    current_position = calculate_position(current_position, next_direction)

    if current_position == start:
        break
    i, j = current_position
    previous_direction = INVERT_DIRECTION[next_direction]
    next_direction = PIPES[maze[i][j]][previous_direction]

print("Part 1", int(route_len / 2))

n_pipes_route = len(marked)

marked_route = marked.copy() # keep route so we can substract it from the marked tiles later (for debugging)


# walk through the pipes again to mark the inside if the route
current_position = start # S

# start in same direction
previous_direction, next_direction = start_from_direction, start_next_direction

while True:
    # mark position on the left/right side of current tile (depending if left or right is inside)
    for direction in [NORTH, EAST, SOUTH, WEST]:
        if left_or_right(DIRECTIONS[next_direction], DIRECTIONS[direction]) == np.sign(turns):
            mark_position = calculate_position(current_position, direction)
            if mark_position is not None:
                mark_tiles(mark_position)

    # use direction of bothe ends of the pipe (need to invert incoming, because we go in the other way)
    for direction in [NORTH, EAST, SOUTH, WEST]:
        if left_or_right(DIRECTIONS[INVERT_DIRECTION[previous_direction]], DIRECTIONS[direction]) == np.sign(turns):
            mark_position = calculate_position(current_position, direction)
            if mark_position is not None:
                mark_tiles(mark_position)

    current_position = calculate_position(current_position, next_direction)

    if current_position == start:
        break
    i, j = current_position

    previous_direction = INVERT_DIRECTION[next_direction]
    next_direction = PIPES[maze[i][j]][previous_direction]

marked_inside = marked.difference(marked_route)
n_inside = len(marked_inside)
print("Part 2", n_inside)


# show_maze(maze, marked_inside)

