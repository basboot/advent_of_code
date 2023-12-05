# Using readlines()
file1 = open('q9a.txt', 'r')
lines = file1.readlines()

visited = set()

ROPE_LENGTH = 10

rope = []
for i in range(ROPE_LENGTH):
    rope.append([0, 0])

visited.add(tuple(rope[-1]))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))



def update_tail():
    for i in range(1, ROPE_LENGTH):
        if abs(rope[i - 1][0] - rope[i][0]) < 2 and abs(rope[i - 1][1] - rope[i][1]) < 2:
            # still close enough, don't move
            pass
        else:
            delta = [clamp(rope[i - 1][0] - rope[i][0], -1, 1), clamp(rope[i - 1][1] - rope[i][1], -1, 1)]
            # print(delta)
            rope[i][0] += delta[0]
            rope[i][1] += delta[1]

    # no problem to add without update, because we use a set
    visited.add(tuple(rope[-1]))


for line in lines:
    row = line.rstrip()

    direction, count = row.split(" ")

    # print(f"Move {direction}, {count} times")

    # x = rl, y = up, + = ru
    for _ in range(int(count)):
        match direction:
            case "R":
                rope[0][0] += 1
            case "L":
                rope[0][0] -= 1
            case "U":
                rope[0][1] += 1
            case "D":
                rope[0][1] -= 1

        update_tail()
        # print(rope)


print(rope[0], rope[-1])
print(len(visited))


