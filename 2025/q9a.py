from itertools import combinations
import numpy as np
from shapely import Polygon

with open("q9a.txt") as f:
    tiles = np.array([tuple(map(int, line.rstrip().split(","))) for line in f])

max_area = np.max(np.prod((np.abs(tiles[..., np.newaxis] - np.transpose(tiles))) + 1, axis=1)) # + 1, incl last

print(f"Part 1: {max_area}")

max_area_with_tiles = 0
floor = Polygon(tiles)
for tile1, tile2 in combinations(tiles, 2):
    coords = np.array([tile1, (tile1[0], tile2[1]), tile2, (tile2[0], tile1[1])])
    rect = Polygon(coords)

    if floor.contains(rect):
        max_area_with_tiles = max(max_area_with_tiles, np.prod(np.abs(tile1 - tile2) + 1))

print(f"Part 2: {max_area_with_tiles}")