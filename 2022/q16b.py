import numpy as np

file1 = open('q16a.txt', 'r')
lines = file1.readlines()

valves = {}
valve_ids = []
usable_valve_ids = []
usable_valves = set()

i = 0
iu = 0
for line in lines:
    row = line.rstrip()
    valve_name, flow_rate_str, to_valves_str = row.replace("Valve ", "").replace(" has flow rate=", ";").replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").split(";")
    flow_rate = int(flow_rate_str)
    to_valves = to_valves_str.split(", ")

    valves[valve_name] = {
        "flow_rate": flow_rate,
        "to_valves": to_valves,
        "index": i,
        "usable_index": iu
    }

    valve_ids.append(valve_name)
    i += 1

    if flow_rate > 0:
        usable_valve_ids.append(valve_name)
        usable_valves.add(valve_name)
        iu += 1

print(valves)

print(usable_valve_ids)

expected_rewards = np.zeros([len(valve_ids), 2**len(usable_valve_ids)]) # position

# for each state possible actions -> transistions + instant reward
for time_left in range(1, 30):
    print(f"Time: {time_left}")
    next_expected_rewards = np.zeros([len(valve_ids), 2 ** len(usable_valve_ids)])

    for position in valves:
        for valve_configuration in range(2**len(usable_valve_ids)):
            reward = 0
            # valve could be opened
            if position in usable_valves:
                # and it is still closed
                if valve_configuration & (1 << valves[position]["usable_index"]) == 0:
                    # get reward
                    immediate_reward = valves[position]["flow_rate"] * time_left
                    expected_reward = expected_rewards[valves[position]["index"], valve_configuration | (1 << valves[position]["usable_index"])]

                    reward = immediate_reward + expected_reward

            # or we can move to another position, without opening anything
            for next_position in valves[position]["to_valves"]:
                expected_reward = expected_rewards[valves[next_position]["index"], valve_configuration]
                reward = max(reward, expected_reward) #TODO:?

            # update
            next_expected_rewards[valves[position]["index"], valve_configuration] = reward

    # bellman update ;-)
    expected_rewards = next_expected_rewards
    # print(expected_rewards)




print(expected_rewards[valves["AA"]["index"], 0])