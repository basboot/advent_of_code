import sys

from executing import cache
from fontTools.misc.cython import returns

sys.setrecursionlimit(10000)

file1 = open('q20a.txt', 'r')
lines = file1.readlines()

route = lines[0].rstrip()[1:-1] # don;t neet ^ and $

directions = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1)
}


def follow_routes(route, positions):
    if len(route) == 0:
        return positions
    else:
        if route[0] == '(':
            level = 0
            current = 1
            part = ""
            parts = []
            while not(level == 0 and route[current] == ')'):
                # from left to right, char by char ( = + 1, ) = -1
                if route[current] == '(':
                    level += 1
                if route[current] == ')':
                    level -= 1
                # split on | when still at level 0
                if route[current] == '|' and level == 0:
                    parts.append(part)
                    part = ""
                else:
                    part += route[current]
                current += 1

            # add last part
            parts.append(part)

            assert len(parts) > 0, "No parts?"
            next_positions = []
            for part in parts:
                next_positions += follow_routes(part, positions)

            return follow_routes(route[current + 1:], next_positions)

        # end on ) at level 0 and remove
        #

        if route[0] in directions:
            di, dj = directions[route[0]]
            next_positions = [(i + di, j + dj) for i, j in positions]


            return follow_routes(route[1:], next_positions)



print(follow_routes(route, [(0, 0)]))


# 107 too low
# 3704 too high