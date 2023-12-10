# Using readlines()
file1 = open('q10a.txt', 'r')
lines = file1.readlines()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

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
next_direction = next(iter(PIPES["S"])) # just get first direction from S

route_len = 0
while True:
    route_len += 1
    current_position = calculate_position(current_position, next_direction)

    if current_position == start:
        break
    i, j = current_position
    next_direction = PIPES[maze[i][j]][INVERT_DIRECTION[next_direction]]

print(route_len / 2)


