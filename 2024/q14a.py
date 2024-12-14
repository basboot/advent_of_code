import numpy as np

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

WIDTH = 101
HEIGHT = 103

robots = []
for line in lines:
    row = list(map(int, line.rstrip().replace("p=", "").replace(" v=", ",").split(",")))
    robots.append(row)

robots = np.array(robots)

SECONDS = 100

positions = np.zeros((len(robots), 2), dtype=int)
positions[:, 0] = np.mod(robots[:, 0] + SECONDS * robots[:, 2], WIDTH)
positions[:, 1] = np.mod(robots[:, 1] + SECONDS * robots[:, 3], HEIGHT)

top_left = positions[np.logical_and(positions[:,0] < WIDTH // 2, positions[:,1] < HEIGHT // 2)]
top_right = positions[np.logical_and(positions[:,0] > WIDTH // 2, positions[:,1] < HEIGHT // 2)]
bottom_left = positions[np.logical_and(positions[:,0] < WIDTH // 2, positions[:,1] > HEIGHT // 2)]
bottom_right = positions[np.logical_and(positions[:,0] > WIDTH // 2, positions[:,1] > HEIGHT // 2)]

print(f"Part 1 {np.prod([len(top_left), len(top_right), len(bottom_left), len(bottom_right)])}")
