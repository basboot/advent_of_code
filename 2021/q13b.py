file1 = open('q13a.txt', 'r')
file_lines = file1.readlines()

folding_input = False

dots = set()
folds = []
for line in file_lines:
    if line.rstrip() == "":
        folding_input = True
        continue

    if folding_input:
        dir, loc = line.rstrip().replace("fold along ", "").replace("x", "0").replace("y", "1").split("=")
        folds.append((int(dir), int(loc)))
    else:
        x, y = line.rstrip().split(",")
        dots.add((int(x), int(y)))

print(dots)
print(folds)

def fold(dots, dir, loc):
    new_dots = set()
    for dot in dots:
        dot = list(dot)
        if dot[dir] > loc:
            dot[dir] = loc - (dot[dir] - loc)
        new_dots.add(tuple(dot))
    return new_dots

for dir, loc in folds:
    dots = fold(dots, dir, loc)


import matplotlib.pyplot as plt
import numpy as np

xy = np.array(list(dots))

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

plt.scatter(xy[:, 0], -xy[:, 1])
plt.show()