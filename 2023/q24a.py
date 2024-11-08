# Using readlines()

import numpy as np

# efficient intersection check
# https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# return
def paths_intersect(position1, velocity1, position2, velocity2) :
    dp = position1 - position2
    dap = perp(velocity1)

    # print("dap", dap)
    # print("velocity", velocity2)
    denom = np.dot( dap, velocity2.transpose())
    # print("d", denom)
    num = np.dot( dap, dp.transpose() )
    # print("num", num)
    return ((num / denom.astype(float))*velocity2.transpose() + position2.transpose()).transpose()


file1 = open('q24a.txt', 'r')
lines = file1.readlines()

stones = []
for line in lines:
    row = [int (x) for x in line.rstrip().replace(" @" , ",").replace(", " , ",").split(",")]
    stones.append(row)

# columns: x y z dx dy dz
stones = np.array(stones)

# toy
MIN = 7
MAX = 27

# real
MIN = 200000000000000
MAX = 400000000000000

# # try to exclude lines that do not intersect the area... DID NOT WORK, NOT USED
# # dy dx
# for corner in [(MIN, MIN), (MIN, MAX), (MAX, MIN), (MAX, MAX)]:
#     x, y = corner
#
#     pos_min_pos = (stones[:, 0:2] - np.array(corner))
#     vecs = stones[:, [4, 3]]
#     dot = np.zeros((len(stones), 1))
#     for i in range(len(stones)):
#         dot[i, 0] = np.dot(pos_min_pos[i,:], vecs[i, :])
#
#     stones = np.concatenate((stones, dot), axis=1)
#
# crossing = np.zeros((len(stones), 1))
# for i in range(len(stones)):
#     mixed = False
#     s = np.sign(stones[i, 6])
#     for j in range(7, 10):
#         if np.sign(stones[i, 6]) != s:
#             mixed = True
#     crossing[i, 0] = 1
#
# stones = np.concatenate((stones, crossing), axis=1)
#
# condition = ((stones[:, 9] > 1))

# print("before", len(stones))
# # remove stones not intersecting rectangle
# stones = stones[condition, :]
# print("after", len(stones))

total = 0
# find all intersections
for i in range(1, len(stones)):
    pos1, vel1 = stones[i-1,0:2], stones[i-1,3:5]
    pos2, vel2 = stones[i:,0:2], stones[i:,3:5]

    intersections = paths_intersect(pos1, vel1, pos2, vel2)
    time1 = (intersections - pos1) / vel1
    time2 = (intersections - pos2) / vel2

    # x y time1 time1 time2 time2
    result = np.concatenate((intersections, time1, time2), axis=1)
    # within rectangle and in the future
    condition = np.sum((result[:, 0] >= MIN) & (result[:, 1] >= MIN) & (result[:, 0] <= MAX)  & (result[:, 1] <= MAX) & (result[:, 2] >= 0) & (result[:, 4] >= 0))

    total += condition

print("Total", total)






# 4108 too low














