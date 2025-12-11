from collections import defaultdict

import networkx as nx
from networkx.algorithms.simple_paths import all_simple_paths

connections = {}

with open("q11a.txt") as f:
    for line in f:
        from_device, to_devices = line.strip().split(": ")
        to_devices = to_devices.split(" ")

        connections[from_device] = to_devices


def number_of_paths(current, goal, number_of_paths_to_goal):
    if current == goal:
        return 1
    if current in number_of_paths_to_goal:
        return number_of_paths_to_goal[current]
    if current not in connections:
        return 0
    for next_device in connections[current]:
        number_of_paths_to_goal[current] += number_of_paths(next_device, goal, number_of_paths_to_goal)
    return number_of_paths_to_goal[current]


print(f"Part 1 {number_of_paths("you", "out", defaultdict(int))}")

svr_dac = number_of_paths("svr", "dac", defaultdict(int))
dac_fft = number_of_paths("dac", "fft", defaultdict(int))
fft_out = number_of_paths("fft", "out", defaultdict(int))

svr_fft = number_of_paths("svr", "fft", defaultdict(int))
fft_dac = number_of_paths("fft", "dac", defaultdict(int))
dac_out = number_of_paths("dac", "out", defaultdict(int))

print(f"Part 2: {svr_dac * dac_fft * fft_out + svr_fft * fft_dac * dac_out}")

