file1 = open('q6a.txt', 'r')
lines = file1.readlines()

direction = -1j
start = 0j
obstacles = set()

for i, line in enumerate(lines):
    for j, value in enumerate(list(line.rstrip())):
        match value:
            case '^':
                start = j + i * 1j
            case '#':
                obstacles.add(j + i * 1j)

grid_size = len(lines) # grid is a rectangle

def find_path_outside(guard, path, obstacles, place_obstacle=False):
    position, direction = guard

    loops = 0
    tried = set()
    while -1 < position.real < grid_size and -1 < position.imag < grid_size:
        next_position = position + direction

        if next_position in obstacles:
            direction *= 1j
        else:
            if place_obstacle and next_position not in tried and (-1 < next_position.real < grid_size and -1 < next_position.imag < grid_size):
                tried.add(next_position) # do not try again, if crossing the same point, because if obstacle is here the guard will not follow this path anymore
                if find_path_outside((position, direction), path.copy(), obstacles.union({next_position}), False) is None:
                    loops += 1
            position = next_position

        if (position, direction) in path:
            return None # None = loop (because the guard visited same position in same direction twice during a walk

        path.add((position, direction))

    return path, loops

path, loops = find_path_outside((start, -1j), set(), obstacles, True)
print("Part 1", len(set([x for x, _ in (path)])))
print("Part 2", loops)
