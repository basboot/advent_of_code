import math
from collections import Counter
import numpy as np
from scipy.signal import convolve2d

serialnumber = 8199

SIZE = 300

# LET OP X Y vs I J

grid = np.zeros((SIZE, SIZE))

grid += np.array(range(1, SIZE + 1)) + 10


rack_id = grid.copy()

grid *= np.transpose(np.array(range(1, SIZE + 1), ndmin=2))


grid += serialnumber

grid = np.multiply(grid, rack_id)

grid = np.mod(grid, 1000) // 100 - 5

print(grid)


result = convolve2d(grid, np.ones((3, 3)), mode='valid')
index_2d = np.unravel_index(np.argmax(result), result.shape)
max_value = np.max(result)
print(f"Part 1, The index of the maximum value is: {index_2d}, value is: {max_value}")

best_value = -math.inf
answer = None

for i in range(1, 300):
    print(i)
    result = convolve2d(grid, np.ones((i, i)), mode='valid')
    index_2d = np.unravel_index(np.argmax(result), result.shape)
    max_value = np.max(result)
    if max_value > best_value:
        best_value = max_value
        answer = (index_2d, i)
        print(answer)

print(f"Part 2, The best result is: {answer}, do not forget to swap i and j for x and y")







