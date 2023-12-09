# Using readlines()
file1 = open('q19a.txt', 'r')
lines = file1.readlines()

import numpy as np

blueprints = {}

for line in lines:
    blueprint_id, r_ore_ore, r_clay_ore, r_obs_ore, r_obs_clay, r_geo_ore, r_geo_obs = [int(x) for x in line.rstrip().replace("Blueprint ", "").replace(" Each ore robot costs ", "").replace(" ore. Each clay robot costs ", ":").replace(" ore. Each obsidian robot costs ", ":").replace(" ore and ", ":").replace(" clay. Each geode robot costs ", ":").replace(" ore and ", ":").replace(" obsidian.", "").split(":")]
    # print(blueprint_id, r_ore_ore, r_clay_ore, r_obs_ore, r_obs_clay, r_geo_ore, r_geo_obs)

    blueprints[blueprint_id] = {
        "r_ore": np.array([r_ore_ore, 0, 0]),
        "r_clay": np.array([r_clay_ore, 0, 0]),
        "r_obs": np.array([r_obs_ore, r_obs_clay, 0]),
        "r_geo": np.array([r_geo_ore, 0, r_geo_obs])
    }

print(blueprints)
# you have exactly one ore-collecting robot
# Each robot can collect 1 of its resource type per minute.
# It also takes one minute for the robot factory to construct any type of robot,

# initial robots and resources
robots = {
    "r_ore": 1,
    "r_clay": 0,
    "r_obs": 0,
    "r_geo": 0
}

resources = np.array([0, 0, 0]) # ore, clay, obs

def possible_actions (blueprint, resources):
    actions = [(None, resources)] # not building a robot (to save resources) is always an option
    # no need to check for multiple robots, because the factory can produce only one
    for robot in blueprint:
        resources_left = resources - blueprint[robot]
        # no resource should be below 0 after building a robot
        if not (np.any((resources_left) < 0)):
            actions.append((robot, resources_left))
    return actions

MAX_TIME = 24

def dfs(blueprint, robots, resources, time):  # function for dfs
    if time == 10:
        print(time)
    if time > MAX_TIME:
        return robots["r_geo"] # number of geodes

    # resources are created after each timestep, so start creating resources after time 0
    if time > 0:
        # make copy, to be sure we keep the original values intact
        resources = resources.copy() + np.array([robots["r_ore"], robots["r_clay"], robots["r_obs"]])


    max_geodes = robots["r_geo"]
    for action in possible_actions(blueprint, resources):
        new_robot, next_resources = action
        next_robots = robots.copy()

        # add new robot
        # it is possible that no robot can be created, or we decide not to, to save resources
        if new_robot is not None:
            next_robots[new_robot] += 1 # don't have to update geodes, will happen in next dfs

        max_geodes = max(max_geodes, dfs(blueprint, next_robots, next_resources, time + 1))

    return max_geodes

dfs(blueprints[1], robots, resources, 0)