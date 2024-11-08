# Using readlines()
import math
from copy import deepcopy

import numpy as np

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

MAX_TIME = 26

# only used to create the map
def bfs(position, explored, goal, queue): #function for BFS
    queue.append((position, []))

    while queue:
        current_position, route = queue.pop(0)
        explored.add(current_position)

        # bfs always finds shortes first, so return immediately
        if current_position == goal:
            return True, len(route)

        for next_position in rooms[current_position]["to_valves"]:
            if next_position not in explored:
                queue.append((next_position, route + [current_position]))

    # no more to explore, and not found the goal
    return False, 0

rooms = {}
valves = {}

valve_names = []

# read data
for line in lines:
    row = line.rstrip()
    room_name, flow_rate_str, to_valves_str = row.replace("Valve ", "").replace(" has flow rate=", ";").replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").split(";")
    flow_rate = int(flow_rate_str)
    to_valves = to_valves_str.split(", ")

    # find all rooms and passages to create the full network
    rooms[room_name] = {
        "flow_rate": flow_rate,
        "to_valves": to_valves
    }

    # find all rooms with a working valve to create the condensed network
    if flow_rate > 0:
        valves[room_name] = {
            "flow_rate": flow_rate,
            "tunnels": []
        }

        # list with the valves for administration (=ids)
        valve_names.append(room_name)


# add room AA to condensed network, because it's the starting point
assert rooms["AA"]["flow_rate"] == 0, "The algorithm assumes the valve at starting point AA is not working"
valves["AA"] = {
    "flow_rate": 0,
    "tunnels": []
}

# create connections in condensed network
for valve_start in valves: # all valves including startpoint
    for valve_goal in valve_names: # only operation valves (no need to go back to start)
        reached, route_len = bfs(valve_start, set(), valve_goal, [])
        assert "reached", "Network is not fully reachable"

        valves[valve_start]["tunnels"].append(route_len + 1) # +1 for opening the valve (there is no other purpose in the condensed network)

flows = np.array([valves[valve]["flow_rate"] for valve in valve_names])

print(flows)

best_pressure = -math.inf

def dfs(visited, players, pressure, remaining_flows):  # function for dfs
    global best_pressure
    # players = 2 x player(location), time
    # choose active player

    # the player with the lowest clock can make the first move
    if players[0][1] < players[1][1]:
        active_player = 0
    else:
        active_player = 1

    player, time = players[active_player]

    if time >= MAX_TIME:
        # update global best result so far
        best_pressure = max(best_pressure, pressure)
        return pressure

    max_new_pressure = pressure
    for i in range(len(valve_names)):
        next_valve = valve_names[i]
        if next_valve in visited: # do not revisit nodes from the same path (also excludes self)
            continue
        cost = valves[player]["tunnels"][i]

        # update time before continuing to next node
        next_time = time + cost

        # create optimistic pressure estimation for this action
        optimistic_pressure_estimation = pressure + sum(remaining_flows) * (MAX_TIME - next_time)
        # don't explore this path any further is the optimistic estimation is worse than what we already have found
        if optimistic_pressure_estimation < best_pressure:
            # print("PRUNE")
            continue

        # update remaining flows (remove valve we open now)
        next_remaining_flows = remaining_flows.copy()
        next_remaining_flows[i] = 0

        # prevent visiting same node again
        next_visited = visited.copy()
        next_visited.add(next_valve)

        # update pressure (if time permits)
        next_pressure = pressure
        if next_time < MAX_TIME:
            next_pressure += valves[next_valve]["flow_rate"] * (MAX_TIME - next_time)

        # update location and time (in copy) for active player in next round
        next_players = deepcopy(players)
        next_players[active_player][0] = next_valve
        next_players[active_player][1] = next_time

        new_pressure = dfs(next_visited, next_players, next_pressure, remaining_flows)
        max_new_pressure = max(max_new_pressure, new_pressure)

    return max_new_pressure


# add tunnels to the
print(valve_names)
print(valves)

# print(bfs("BB", set(), "JJ", []))
print(dfs(set(), [["AA", 0], ["AA", 0]], 0, flows))