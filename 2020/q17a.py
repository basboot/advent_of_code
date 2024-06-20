file1 = open('q17a.txt', 'r')
lines = file1.readlines()

cubes = set()

for i in range(len(lines)):
    line = list(lines[i].rstrip())
    for j in range(len(lines)):
        if line[j] == "#": # only store active
            cubes.add((i, j, 0)) # Note: we use 0 indexing nstead of 1!

def count_and_update_neighbours(cube, cubes, neighbour_count):
    x, y, z = cube
    neighbours = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                if i == j == k == 0:
                    continue # don't count self
                position = (x + i, y + j, z + k)
                if position in cubes:
                    neighbours += 1
                else:
                    if position not in neighbour_count:
                        neighbour_count[position] = 1
                    else:
                        neighbour_count[position] += 1
    return neighbours

n_generations = 6

for gen in range(n_generations):
    neighbour_count = {}
    next_generation = set()
    for cube in cubes:
        neighbours = count_and_update_neighbours(cube, cubes, neighbour_count)
        # cube survives is it has exactly 2 or 3 neighbours
        if neighbours == 2 or neighbours == 3:
            next_generation.add(cube)
    for cube, neighbours in neighbour_count.items(): # cube spawns if empty space has exactly 3 neighbours
        if neighbours == 3:
            next_generation.add(cube)

    print(neighbour_count)

    print(gen, len(next_generation))
    cubes = next_generation







