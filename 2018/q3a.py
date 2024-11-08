import numpy as np

file1 = open('q3a.txt', 'r')
lines = file1.readlines()

fabric = np.zeros((1000, 1000))

for line in lines:
    id, left, top, width, height = [int(x) for x in line.rstrip().replace("#", "").replace("@ ", "").replace(",", " ").replace(":", "").replace("x", " ").split(" ")]

    patch = np.ones((height, width))
    # print(patch)

    fabric[top:top + height, left: left + width] += patch

# print(fabric)

print("Part 1", np.sum(fabric > 1))

for line in lines:
    id, left, top, width, height = [int(x) for x in line.rstrip().replace("#", "").replace("@ ", "").replace(",", " ").replace(":", "").replace("x", " ").split(" ")]

    patch = np.ones((height, width))
    # print(patch)

    if (np.sum(fabric[top:top + height, left: left + width] - patch) == 0):
        print("Part 2", id)
        break
