# Using readlines()
import math

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



# initial robots and resources
robots = {
    ORE: 1,
    CLAY: 0,
    OBS: 0,
    GEO: 0
}


resources = np.array([0, 0, 0, 0]) # ore, clay, obs, geode

def possible_actions (blueprint, resources, robots, time_left):
    actions = [(None, resources)] # not building a robot (to save resources) is always an option
    # no need to check for multiple robots, because the factory can produce only one
    for robot in blueprint:
        # if we can produce enough resources to build a robot each timestep we can stop creating a resource robot
        if robot == OBS:
            if robots[OBS] >= blueprint[GEO][OBS]:
                continue
            if time_left < 3:
                continue
        if robot == CLAY:
            if robots[CLAY] >= blueprint[OBS][CLAY] / 2:
                continue
            if time_left < 3:
                continue
        if robot == ORE:
            if robots[ORE] >= max(blueprint[ORE][ORE], blueprint[CLAY][ORE], blueprint[OBS][ORE], blueprint[GEO][ORE]):
                continue
            if time_left < 3:
                continue

        resources_left = resources - blueprint[robot]
        # no resource should be below 0 after building a robot
        if not (np.any((resources_left) < 0)):
            actions.append((robot, resources_left))
    return actions

MAX_TIME = 24

best_geo = -math.inf

def dfs(blueprint, robots, resources, time):  # function for dfs
    # resources are created after each timestep, so start creating resources after time 0
    if time > 0:
        # make copy, to be sure we keep the original values intact
        resources = resources.copy() + np.array([robots[ORE], robots[CLAY], robots[OBS], robots[GEO]])

    global best_geo

    # TODO Fix best estim
    # we cannot hope to create more than one robot per timestep
    # optimistic_estimation = MAX_TIME - time + robots[GEO]
    #
    # if optimistic_estimation < best_geo:
    #     return 0


    if time > MAX_TIME:
        # best_geo = max(robots[GEO], best_geo)
        if best_geo < resources[GEO]:
            best_geo = resources[GEO]
            print(best_geo)
        return robots[GEO] # number of geodes



    max_geodes = resources[GEO]
    for action in possible_actions(blueprint, resources, robots, MAX_TIME - time):
        new_robot, next_resources = action
        next_robots = robots.copy()

        # add new robot
        # it is possible that no robot can be created, or we decide not to, to save resources
        if new_robot is not None:
            next_robots[new_robot] += 1 # don't have to update geodes, will happen in next dfs

        max_geodes = max(max_geodes, dfs(blueprint, next_robots, next_resources, time + 1))

    return max_geodes


dfs(blueprints[1], robots, resources, 0)