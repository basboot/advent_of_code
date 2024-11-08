import numpy as np

file1 = open('q6a.txt', 'r')

# ChatGPT
def create_manhattan_distance_lookup(N, M, x0, y0):
    x = np.arange(N)[:, None]  # Create a column vector of row indices
    y = np.arange(M)  # Create a row vector of column indices

    # Calculate the Manhattan distances using broadcasting
    distance_table = np.abs(x - x0) + np.abs(y - y0)

    return distance_table

DISTANCE = 10000

# 50 places, so max we need to check is 10000 / 50 * 2 = 400, range if the places is also about 400, so use 1200

# manhattan set, defined by corners, start with top, the clockwise
combined_distances = np.zeros((1200, 1200)) # create large enough
for line in file1.readlines():
    x, y = [int(x) for x in line.rstrip().split(", ")]
    combined_distances += create_manhattan_distance_lookup(1200, 1200, x + 400, y + 400)

print(np.sum(combined_distances < DISTANCE))


