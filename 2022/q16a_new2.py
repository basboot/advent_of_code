# Using readlines()

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

MAX_TIME = 30

# BFS algorithm


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

# def bfs_old(position, explored, route, goal):
#     # print(position, route)
#     if position == goal:
#         # print(f"Reached goal with route length {len(route)} ({route})")
#         return True, len(route)
#
#     # stop path when already explored
#     if position in explored:
#         return False, 0
#     # avoid exploring again
#     explored.add(position)
#
#     for next_position in rooms[position]["to_valves"]:
#         reached, route_len = bfs(next_position, explored, route + [next_position], goal)
#         if reached:
#             return reached, route_len
#
#     return False, 0

rooms = {}
valves = {}

valve_names = []

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



def dfs(visited, node, time, pressure):  # function for dfs
    if time > MAX_TIME:
        return pressure
    else:
        # add pressure for last opened valve (for remaining time)
        pressure += valves[node]["flow_rate"] * (MAX_TIME - time)

    # print (node)
    visited.add(node)
    max_new_pressure = pressure
    for i in range(len(valve_names)):
        next_valve = valve_names[i]
        if next_valve in visited: # do not revisit nodes from the same path (also excludes self)
            continue
        cost = valves[node]["tunnels"][i]
        new_pressure = dfs(visited.copy(), next_valve, time + cost, pressure)
        max_new_pressure = max(max_new_pressure, new_pressure)

    return max_new_pressure



# add tunnels to the
print(valve_names)
print(valves)

# print(bfs("BB", set(), "JJ", []))
print(dfs(set(), "AA", 0, 0))