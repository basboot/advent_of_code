from collections import defaultdict
from itertools import combinations

file1 = open('q8a.txt', 'r')
lines = file1.readlines()

antennas = defaultdict(list)

for i, row in enumerate(lines):
    for j, value in enumerate(list(row.strip())):
        if value != '.':
            antennas[value].append(i + j * 1j)

grid_size = len(lines)
assert grid_size == len(lines[0].rstrip()), "Grid is not rectangular"

def find_antinodes(frequency):
    antinodes = []
    for antenna1, antenna2 in combinations(antennas[frequency], 2):
        delta = antenna2 - antenna1
        antinodes.append(antenna1 - delta)
        antinodes.append(antenna2 + delta)

    return set(filter(lambda pos: -1 < pos.real < grid_size and -1 < pos.imag < grid_size, antinodes))

def find_antinodes_resonant(frequency):
    antinodes = []
    for antenna1, antenna2 in combinations(antennas[frequency], 2):
        delta = antenna2 - antenna1
        pos = antenna1
        while -1 < pos.real < grid_size and -1 < pos.imag < grid_size:
            antinodes.append(pos)
            pos = pos - delta

        pos = antenna2
        while -1 < pos.real < grid_size and -1 < pos.imag < grid_size:
            antinodes.append(pos)
            pos = pos + delta

    return set(filter(lambda pos: -1 < pos.real < grid_size and -1 < pos.imag < grid_size, antinodes))

antinodes1 = set()
antinodes2 = set()

for frequency in antennas:
    antinodes1 = antinodes1.union(find_antinodes(frequency))
    antinodes2 = antinodes2.union(find_antinodes_resonant(frequency))

print(f"Part 1, {len(antinodes1)}")
print(f"Part 2, {len(antinodes2)}")

