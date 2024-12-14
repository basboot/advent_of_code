file1 = open('q12a.txt', 'r')
lines = file1.readlines()

garden = {}

for i, row in enumerate(lines):
    for j, value in enumerate(list(row.rstrip())):
        garden[(i, j)] = value

garden_size = len(lines)

def count_region(position, current_region, perimeter_edges):
    current_region.add(position)
    area = 1
    perimeter = 0
    i, j = position
    value = garden[(i, j)]

    for di, dj, direction in [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]:
        ni, nj = i + di, j + dj
        next_position = (ni, nj)
        if next_position in current_region:
            continue # no double visit
        if next_position not in garden or garden[next_position] != value:
            perimeter += 1
            # add current position to perimeter edges
            perimeter_edges.add((i, j, direction))
            continue

        next_area, next_perimeter, _, _ = count_region(next_position, current_region, perimeter_edges)

        area += next_area
        perimeter += next_perimeter

    return area, perimeter, current_region, perimeter_edges

visited = set()

perpendicular_directions = {
    'u': ((0, -1), (0, 1)),
    'd': ((0, -1), (0, 1)),
    'l': ((-1, 0), (1, 0)),
    'r': ((-1, 0), (1, 0)),
}

def count_sides(perimeter_edges):
    sides = 0
    while len(perimeter_edges) > 0:
        edge = set()
        # get random point
        point = list(perimeter_edges)[0]
        edge.add(point)

        for di, dj in perpendicular_directions[point[2]]:
            i, j, direction = point

            while (i + di, j + dj, direction) in perimeter_edges:
                edge.add((i + di, j + dj, direction))
                i += di
                j += dj

        perimeter_edges = perimeter_edges - edge
        sides += 1

    return sides

total = 0
total2 = 0

for i in range(garden_size):
    for j in range(garden_size):
        if (i, j) in visited:
            continue # no double

        area, perimeter, next_visited, perimeter_edges = count_region((i, j), set(), set())
        visited = visited.union(next_visited)

        sides = count_sides(perimeter_edges)

        total += area * perimeter
        total2 += area * sides

print(f"Part 1, {total}")
print(f"Part 2, {total2}")
