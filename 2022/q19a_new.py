# Using readlines()
import heapq
import math

from itertools import count

file1 = open('q19a.txt', 'r')
lines = file1.readlines()

import numpy as np

blueprints = {}
ORE, CLAY, OBS, GEO = 0, 1, 2, 3

for line in lines:
    blueprint_id, r_ore_ore, r_clay_ore, r_obs_ore, r_obs_clay, r_geo_ore, r_geo_obs = [int(x) for x in line.rstrip().replace("Blueprint ", "").replace(" Each ore robot costs ", "").replace(" ore. Each clay robot costs ", ":").replace(" ore. Each obsidian robot costs ", ":").replace(" ore and ", ":").replace(" clay. Each geode robot costs ", ":").replace(" ore and ", ":").replace(" obsidian.", "").split(":")]
    # print(blueprint_id, r_ore_ore, r_clay_ore, r_obs_ore, r_obs_clay, r_geo_ore, r_geo_obs)

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

def possible_actions (blueprint, resources, robots, t):
    actions = [(MAX_TIME - robots[GEO], robots, resources, t + 1)] # not building a robot (to save resources) is always an option
    # no need to check for multiple robots, because the factory can produce only one
    for robot in blueprint:
        resources_left = resources - blueprint[robot]
        # no resource should be below 0 after building a robot
        new_robots = robots.copy()
        if not (np.any((resources_left) < 0)):
            new_robots[robot] += 1
            actions.append((MAX_TIME - robots[GEO], new_robots, resources_left, t + 1)) # TODO: calculate cost
    return actions

MAX_TIME = 24


def dijkstra(robots, resources, blueprint):
    explored = set()
    to_explore = []  # heapq (estimated_cost, cost_so_far, pos, direction, n_straight)

    counter = count() # solve problem np comparison in heap

    # push start with no cost (as stated in assignment) to heap
    heapq.heappush(to_explore, (MAX_TIME, next(counter), robots, resources, 0))


    while len(to_explore) > 0:
        cost, _, robots, resources, t = heapq.heappop(to_explore)
        print(t)
        if t == MAX_TIME:
            print("FOUND", resources)
            continue

        # update resources
        if t > 0:
            # make copy, to be sure we keep the original values intact
            resources = resources.copy() + np.array([robots[ORE], robots[CLAY], robots[OBS], robots[GEO]])


        actions = possible_actions(blueprint, resources, robots, t)
        # print(actions)

        for next_cost, next_robots, next_resources, next_t in actions:
            if (frozenset(next_robots.items()), next_resources.data.tobytes(), next_t) in explored:  # don't explore again (without cost, because earlies is always better)
                continue # TODO: do we have to look at t?

            if next_t > MAX_TIME:
                continue


            # print(">>>", next_cost, next_robots, next_resources, next_t)
            # print(heapq)
            heapq.heappush(to_explore, (cost + next_cost, next(counter), next_robots, next_resources, next_t))
            explored.add(
                (frozenset(next_robots.items()), next_resources.data.tobytes(), next_t))  # TODO: is this the right place?

    return "Not found"


# initial robots and resources
robots = {
    ORE: 1,
    CLAY: 0,
    OBS: 0,
    GEO: 0
}

resources = np.array([0, 0, 0, 0]) # ore, clay, obs, geode

print(dijkstra(robots, resources, blueprints[1]))


# push start with no cost (as stated in assignment) to heap

