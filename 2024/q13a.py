file1 = open('q13a.txt', 'r')
lines = file1.readlines()

import numpy as np

total = 0

part = 2

for i in range(0, len(lines), 4):
    ax, ay = [int(x) for x in lines[i].rstrip().split(": ")[1].replace("X+", "").replace("Y+", "").split(", ")]
    bx, by = [int(x) for x in lines[i + 1].rstrip().split(": ")[1].replace("X+", "").replace("Y+", "").split(", ")]
    rx, ry = [int(x) + 10000000000000 * (part - 1) for x in lines[i + 2].rstrip().split(": ")[1].replace("X=", "").replace("Y=", "").split(", ")]

    a = np.array([[ax, bx], [ay, by]])
    b = np.array([rx, ry])
    x = np.linalg.solve(a, b)
    sa, sb = [round(s) for s in x]
    if sa * ax + sb * bx == rx and sa * ay + sb * by == ry:
        total += 3*sa + sb

print(f"Part {part}, {total}")

# 26658 too low (// 1 te heftig, round beter)
