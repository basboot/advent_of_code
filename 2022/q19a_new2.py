# Using readlines()

file1 = open('q19a.txt', 'r')
lines = file1.readlines()

from collections import deque

import numpy as np

blueprints = {}
ORE, CLAY, OBS, GEO = 0, 1, 2, 3

for line in lines:
    blueprint_id, r_ore_ore, r_clay_ore, r_obs_ore, r_obs_clay, r_geo_ore, r_geo_obs = [int(x) for x in line.rstrip().replace("Blueprint ", "").replace(" Each ore robot costs ", "").replace(" ore. Each clay robot costs ", ":").replace(" ore. Each obsidian robot costs ", ":").replace(" ore and ", ":").replace(" clay. Each geode robot costs ", ":").replace(" ore and ", ":").replace(" obsidian.", "").split(":")]

    blueprints[blueprint_id] = {
        ORE: np.array([r_ore_ore, 0, 0, 0]),
        CLAY: np.array([r_clay_ore, 0, 0, 0]),
        OBS: np.array([r_obs_ore, r_obs_clay, 0, 0]),
        GEO: np.array([r_geo_ore, 0, r_geo_obs, 0])
    }

print(blueprints)
# you have exactly one ore-collecting robot
# Each robot can collect 1 of its resource type per minute.
# It also takes one minute for the robot factory to construct any type of robot,

def possible_actions (blueprint, resources, robots, t_left, robots_you_could_buy_before):

    # no need to check for multiple robots, because the factory can produce only one
    actions = []
    robots_you_could_buy = set()
    # don't build on last round
    if t_left > 0:
        for robot in blueprint:
            # don't build robot we could buy earlier
            if robot in robots_you_could_buy_before:
                continue
            # don't build robots we cannot use
            if robot != GEO and robots[robot] >= blueprint[ORE][robot] and \
                robots[robot] >= blueprint[CLAY][robot] and \
                robots[robot] >= blueprint[OBS][robot] and \
                robots[robot] >= blueprint[GEO][robot]:
                # print(robot)
                # print(robots[robot], blueprint[ORE][robot], blueprint[CLAY][robot], blueprint[OBS][robot], blueprint[GEO][robot])
                continue

            resources_left = resources - blueprint[robot]
            # no resource should be below 0 after building a robot
            if not (np.any((resources_left) < 0)):
                new_robots = np.array([0, 0, 0, 0])
                new_robots[robot] = 1
                actions.append((resources_left, new_robots, set()))
                robots_you_could_buy.add(robot)

    # not building a robot (and wait for resources) is always an option
    # add robots you could have bought (to avoid waiting and buying later)
    # remember until a robot has been built
    actions.append((resources, np.array([0, 0, 0, 0]), robots_you_could_buy.union(robots_you_could_buy_before)))

    return actions


def dfs(blueprint, resources, robots, t, MAX_TIME = 24):

    # print("NEXT", t, resources, "<>", robots)

    stack = deque()

    stack.append((resources, robots, t, set()))

    max_resources = np.array([0, 0, 0, 0])

    while len(stack) > 0:
        resources, robots, t, robots_you_could_buy_before = stack.pop()

        # print(t, ".", resources, robots, t, robots_you_could_buy_before)


        if t > MAX_TIME: # > after last minute, stop
            if resources[GEO] > max_resources[GEO]:
                max_resources = resources
                # print("found better", max_resources)
            continue

        # prune branch if we can't do better with an optimistic estimation than the current best (+1, for current)
        optimistic = resources[GEO] + (MAX_TIME - t + 1) * robots[GEO] + ((MAX_TIME - t + 1) * (MAX_TIME - t + 1 + 1)) /2
        if optimistic <= max_resources[GEO]:
            continue


        for resources_left, new_robots, robots_you_could_have_bought in possible_actions(blueprint, resources, robots, MAX_TIME - t, robots_you_could_buy_before):
            # 1. start building (begin of minute)

            # 2. update resources from collecting robots (during minute)
            next_resources = resources_left + robots  # assume never larger that bit size!

            # 3. building finished (end minute)
            next_robots = robots + new_robots

            # go to next minute
            stack.append((next_resources, next_robots, t + 1, robots_you_could_have_bought))


    return max_resources[GEO]

total = 0

for blueprint in blueprints:
    print(f"Blueprint {blueprint}")
    # initial robots and resources
    robots = np.array([1, 0, 0, 0])
    resources = np.array([0, 0, 0, 0])  # ore, clay, obs, geode

    result = dfs(blueprints[blueprint], resources, robots, 1)

    total += (result * blueprint)

print("Total", total)


total = 1
for blueprint in blueprints:
    print(f"Blueprint {blueprint}")
    # initial robots and resources
    robots = np.array([1, 0, 0, 0])
    resources = np.array([0, 0, 0, 0])  # ore, clay, obs, geode

    result = dfs(blueprints[blueprint], resources, robots, 1, 32)

    total *= result

    print("...", blueprint, total)

    if blueprint == 3:
        break # only first 3

print("Total", total)

