import math
from collections import deque
import heapq
import numpy
import numpy as np

machines = []

with open("q10a.txt") as f:
    for line in f:
        # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        pattern_data, temp_data = line.strip().split("] (")
        pattern = tuple([-1 if c == "." else 1 for c in list(pattern_data.replace("[", ""))])
        button_data, joltage_data = temp_data.split(") {")
        button_data = [list(map(int, b.split(","))) for b in button_data.replace("(", "").replace(")", "").split(" ")]
        buttons = []
        joltage_buttons = []
        for button in button_data:
            buttons.append(np.array([-1 if i in button else 1 for i in range(len(pattern))]))
            joltage_buttons.append(np.array([1 if i in button else 0 for i in range(len(pattern))]))

        joltage_pattern = tuple(map(int, joltage_data.replace("}", "").split(",")))

        machines.append((pattern, buttons, joltage_pattern, joltage_buttons))


def find_minimum_number_of_toggles(machine):
    goal, buttons, _, _ = machine
    start = tuple([-1] * len(goal)) # start all off
    to_explore = deque([(start, 0)])
    visited = set()

    while len(to_explore) > 0:
        pattern, n_toggles = to_explore.popleft()

        if pattern == goal:
            return n_toggles

        pattern = np.array(pattern)

        for button in buttons:
            next_pattern = tuple(numpy.multiply(pattern, button))
            if next_pattern in visited:
                continue # bfs, so invalidate early
            else:
                visited.add(next_pattern)
                to_explore.append((next_pattern, n_toggles + 1))

    assert False, "Pattern not possible"

def minimum_number_of_presses_heuristic(goal, pattern):
    presses = np.array(goal) - np.array(pattern)

    if np.any(presses < 0):
        return math.inf # goal not reachable anymore
    else:
        return np.max(presses) # at least this number of presses needed

def find_minimum_number_of_presses(machine):
    _, _, goal, buttons = machine

    start = tuple([0] * len(goal)) # start all zero
    to_explore = [(minimum_number_of_presses_heuristic(goal, start), 0, start)]
    visited = set()

    while len(to_explore) > 0:
        minimum_presses, n_presses, pattern = heapq.heappop(to_explore)

        if pattern == goal:
            return n_presses

        if pattern in visited:
            continue
        visited.add(pattern)

        pattern = np.array(pattern)

        for button in buttons:
            next_pattern = tuple(pattern + button)
            if next_pattern not in visited:
                heapq.heappush(to_explore, (n_presses + 1 + minimum_number_of_presses_heuristic(goal, next_pattern), n_presses + 1, next_pattern))

    assert False, "Pattern not possible"

print(f"Part 1: {sum([find_minimum_number_of_toggles(machine) for machine in machines])}")
# print(f"Part 2: {sum([find_minimum_number_of_presses(machine) for machine in machines])}") # infeasible for large numbers :-(





