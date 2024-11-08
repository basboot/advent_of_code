import math

file1 = open('q17a.txt', 'r')
file_lines = file1.readlines()

# target area: x=20..30, y=-10..-5

# [x _min, x_max, y_min, y_max]
target = [int(x) for x in file_lines[0].replace("target area: x=", "").replace(" y=", "").replace("..", ",").split(",")]

print(target)

def hit_target(vel, target):
    # start
    pos = (0, 0)

    highest_y = -math.inf

    x_min, x_max, y_min, y_max = target

    while True:

        # update
        pos = (pos[0] + vel[0], pos[1] + vel[1])

        # print(pos)

        x, y = pos
        x_vel, y_vel = vel

        highest_y = max(highest_y, y)

        if x_min <= x <= x_max and y_min <= y <= y_max:
            # print("hit", x, y)
            return True, x, y, highest_y

        if y < y_min and y_vel < 0:
            # print("too low")
            return False, x, y, highest_y

        if x > x_max:
            # print("too far")
            return False, x, y, highest_y

        # change vel
        vel = (max(0, vel[0] - 1), vel[1] - 1)


# simple: try all x_vel 1 - max_x <- try y until y > max_y, per x_vel
print(hit_target((17,-4), target))

max_y_vel = -math.inf

def possible_x_vel(target):
    x_min, x_max, y_min, y_max = target

    # TODO: reduce options

    return list(range(1, x_max + 1))

x_min, x_max, y_min, y_max = target

max_highest_y = -math.inf

total = 0
# TODO: can we skip x speed 0?
for x_vel in range(0, x_max + 1): # x speed larger than x_max will overshoot the target at t = 1
    y_vel = 0  # TODO: can be negative?
    print(x_vel)

    for y_vel in range(-500, 500):

        hit, x, y, highest_y = hit_target((x_vel,y_vel), target)

        if hit:
            print("HIT")
            max_y_vel = max(max_y_vel, y_vel)
            max_highest_y = max(max_highest_y, highest_y)
            total += 1


print("Part 1", max_y_vel, max_highest_y)
print("Part 2", total)