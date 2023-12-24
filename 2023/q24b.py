# Using readlines()
from tools.advent_tools import *

import numpy as np

# https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


file1 = open('q24a.txt', 'r')
lines = file1.readlines()

stones = []
for line in lines:
    row = [int (x) for x in line.rstrip().replace(" @" , ",").replace(", " , ",").split(",")]
    stones.append(row)

# columns: x y z dx dy dz
stones = np.array(stones)

from sympy import *

x, y, z = symbols("x,y,z", integer=True) # start position of thrown brick
u, v, w = symbols("u,v,w", integer=True) # speed of brick

stones = stones[0:4] # reduce problem (and variables) => still gives only one solution because the problems contrains

t = symbols(f"t0:{len(stones)}") # collision times


# Tried to use Sage for more speed, but didn't work
# print("x, y, z, u, v, w = var('x, y, z, u, v, w')")
# print(f'{", ".join([str(s) for s in t])} = var(\'{", ".join([str(s) for s in t])}\')')


equations = []

for i in range(len(stones)):
    px, py, pz, dx, dy, dz = stones[i]

    equations.append(x + u * t[i] - px - dx * t[i])
    equations.append(y + v * t[i] - py - dy * t[i])
    equations.append(z + w * t[i] - pz - dz * t[i])

    # print(f"x + u * t{i} - {px} - {dx} * t{i} == 0, ", end="")
    # print(f"y + v * t{i} - {py} - {dy} * t{i} == 0, ", end="")
    # print(f"z + w * t{i} - {pz} - {dz} * t{i} == 0, ", end="")


# print("], x, y, z, u, v, w, ", end="")
# print(f'{", ".join([str(s) for s in t])})')

solution = solve(equations, [x, y, z, u, v, w] + list(t))

print("Total", (solution[0][0] + solution[0][1] + solution[0][2]))

# print(solution)








