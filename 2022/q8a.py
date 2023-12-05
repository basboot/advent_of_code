import numpy as np

# Using readlines()
file1 = open('q8a.txt', 'r')
lines = file1.readlines()

def tree_score(i, j, forrest):
    height = forrest[i, j]
    # print(height)
    m, n = forrest.shape

    tree_score = 1

    visible_trees = 0
    # left
    for li in range(i - 1, -1, -1):
        if forrest[li, j] >= height:
            visible_trees += 1 # blocking tree also counts
            break
        visible_trees += 1

    tree_score *= visible_trees

    visible_trees = 0
    # right
    for li in range(i + 1, m):
        if forrest[li, j] >= height:
            visible_trees += 1 # blocking tree also counts
            break
        visible_trees += 1
    tree_score *= visible_trees

    visible_trees = 0
    # top
    for lj in range(j - 1, -1, -1):
        if forrest[i, lj] >= height:
            visible_trees += 1 # blocking tree also counts
            break
        visible_trees += 1
    tree_score *= visible_trees

    visible_trees = 0
    # bottom
    for lj in range(j + 1, n):
        if forrest[i, lj] >= height:
            visible_trees += 1 # blocking tree also counts
            break
        visible_trees += 1
    tree_score *= visible_trees

    return tree_score

#1695
def is_visible(i, j, forrest):
    height = forrest[i, j]
    m, n = forrest.shape

    visible_sides = 4
    # left
    for li in range(0, i):
        if forrest[li, j] >= height:
            visible_sides -= 1
            break
    # right
    for li in range(i + 1, m):
        if forrest[li, j] >= height:
            visible_sides -= 1
            break
    # top
    for lj in range(0, j):
        if forrest[i, lj] >= height:
            visible_sides -= 1
            break
    # bottom
    for lj in range(j + 1, n):
        if forrest[i, lj] >= height:
            visible_sides -= 1
            break

    # no sides have larger trees
    return visible_sides > 0

def is_visible_old(i, j, forrest):
    height = forrest[i, j]
    m, n = forrest.shape

    # on the edge, is always visble
    if i == 0 or j == 0 or i == m - 1 or j == n - 1:
        return True

    # left
    if np.max(forrest[:i, j]) < height:
        return True
    # right
    if np.max(forrest[i+1:, j]) < height:
        return True
    # top
    if np.max(forrest[i, :j]) < height:
        return True
    # bottom
    if np.max(forrest[i, j+1:]) < height:
        return True

    # all sides have larger trees
    return False



forrest = []
for line in lines:
    row = line.rstrip()
    # print("input: ", row)

    trees = []
    for c in row:
        trees.append(int(c))
    forrest.append(trees)

forrest = np.array(forrest)

m, n = forrest.shape

total = 0
for i in range(m):
    for j in range(n):
        # print(f"{i}, {j}, {is_visible(i, j, forrest)}")
        if is_visible(i, j, forrest):
            total += 1

print(total)

# print(tree_score(1, 2, forrest))

score = 0
for i in range(m):
    for j in range(n):
        score = max(score, tree_score(i, j, forrest))
print(score)


