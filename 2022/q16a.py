# Using readlines()
import collections
import math

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

MAX_TIME = 30

# change to coverage search
# https://github.com/rodriguesrenato/coverage-path-planning

# BFS algorithm
def bfs_uncovered(root, covered, time_left):
    queue = collections.deque([(root, [], 0, set(), covered)])
    # visited.add(root)
    solutions = []

    while queue:
        # Dequeue a vertex from queue
        vertex, route, time_spent, visited_on_route, covered = queue.popleft()
        # print(queue)

        # # skip explored nodes
        # if vertex in visited:
        #     continue
        #
        # visited.add(vertex)

        if vertex not in covered:
            # found a solution
            solutions.append((vertex, route, time_spent)) # open +1
            covered = covered.copy()
            covered.add(vertex)
            # all valves have been tried on this route
            if len(covered) == len(valves) or time_spent > time_left:
                continue


        for neighbour in valves[vertex]["to_valves"]:
            if neighbour not in visited_on_route:
                new_visited = visited_on_route.copy()
                new_visited.add(neighbour)
                queue.append((neighbour, route + [neighbour], time_spent + 1, new_visited, covered)) # move = 1

    return solutions

def bfs(root):

    queue = collections.deque([(root, [root], 2, set(root), 0)])

    max_pressure = -math.inf

    while queue:

        # Dequeue a vertex from queue
        vertex, route, time_spent, visited, pressure = queue.popleft()
        # print(queue)

        # cover this valve
        visited.add(vertex)

        if time_spent == MAX_TIME:
            if pressure > max_pressure:
                max_pressure = pressure
            print(f"time's up ({route} {pressure})")
            continue


        for solution in bfs_uncovered(vertex, visited, MAX_TIME - time_spent):
            added_vertex, added_route, added_time_spent = solution
            # remove solution if it is not within the time limit
            if time_spent + added_time_spent > MAX_TIME:
                added_route = []
                added_pressure = 0
                added_time_spent = MAX_TIME - time_spent
            else:
                added_pressure = (MAX_TIME - (time_spent + added_time_spent)) * valves[added_vertex]["flow_rate"]

            queue.append((added_vertex, route + added_route, time_spent + added_time_spent, visited.copy(), pressure + added_pressure))

    return max_pressure

valves = {}
for line in lines:
    row = line.rstrip()
    valve_name, flow_rate_str, to_valves_str = row.replace("Valve ", "").replace(" has flow rate=", ";").replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").split(";")
    flow_rate = int(flow_rate_str)
    to_valves = to_valves_str.split(", ")

    valves[valve_name] = {
        "flow_rate": flow_rate,
        "to_valves": to_valves
    }

# print(valves)
#
# bfs("AA")

# print(bfs_uncovered("AA", {"AA"}))

print(bfs("AA"))
# toy example solution 1651


# == Minute 1 ==
# No valves are open.
# You move to valve DD.
#
# == Minute 2 ==
# No valves are open.
# You open valve DD.
#
# == Minute 3 ==
# Valve DD is open, releasing 20 pressure.
# You move to valve CC.
#
# == Minute 4 ==
# Valve DD is open, releasing 20 pressure.
# You move to valve BB.
#
# == Minute 5 ==
# Valve DD is open, releasing 20 pressure.
# You open valve BB.
#
# == Minute 6 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve AA.
#
# == Minute 7 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve II.
#
# == Minute 8 ==
# Valves BB and DD are open, releasing 33 pressure.
# You move to valve JJ.
#
# == Minute 9 ==
# Valves BB and DD are open, releasing 33 pressure.
# You open valve JJ.
#
# == Minute 10 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve II.
#
# == Minute 11 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve AA.
#
# == Minute 12 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve DD.
#
# == Minute 13 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve EE.
#
# == Minute 14 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve FF.
#
# == Minute 15 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve GG.
#
# == Minute 16 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You move to valve HH.
#
# == Minute 17 ==
# Valves BB, DD, and JJ are open, releasing 54 pressure.
# You open valve HH.
#
# == Minute 18 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve GG.
#
# == Minute 19 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve FF.
#
# == Minute 20 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You move to valve EE.
#
# == Minute 21 ==
# Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
# You open valve EE.
#
# == Minute 22 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You move to valve DD.
#
# == Minute 23 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You move to valve CC.
#
# == Minute 24 ==
# Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
# You open valve CC.
#
# == Minute 25 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
#
# == Minute 26 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
#
# == Minute 27 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
#
# == Minute 28 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
#
# == Minute 29 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
#
# == Minute 30 ==
# Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II