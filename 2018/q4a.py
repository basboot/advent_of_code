from collections import Counter
import numpy as np

file1 = open('q4a.txt', 'r')
lines = file1.readlines()


events = [line.rstrip() for line in lines]
events.sort()

guards = {}

def add_sleep(guard, sleep, wake):
    if guard not in guards:
        guards[guard] = [0, np.zeros((60))]

    guards[guard][0] += wake - sleep
    guards[guard][1][sleep:wake] += 1


guard = -1
sleep = -1
wake = -1

for event in events:
    log = event.split(" ")

    match(log[2]):
        case "Guard":
            guard = int(log[3].replace("#", ""))
            print("Guard", guard)
        case "falls":
            print("sleep", int(log[1].replace("]", "").split(":")[1]))
            sleep = int(log[1].replace("]", "").split(":")[1])
        case "wakes":
            print("wakes", int(log[1].replace("]", "").split(":")[1]))
            wake = int(log[1].replace("]", "").split(":")[1])

            add_sleep(guard, sleep, wake)



guard_max = max(guards, key = lambda x: guards[x])
print("The sleepy guard is", guard_max)

minute_max = np.argmax(guards[guard_max][1])
print("Sleeping most at", minute_max)

print("Part 1", guard_max * minute_max)

###


guard_max = max(guards, key = lambda x: np.max(guards[x][1]))
print("The sleepy guard is", guard_max)

minute_max = np.argmax(guards[guard_max][1])
print("Sleeping most at", minute_max)

print("Part 2", guard_max * minute_max)


# [1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
# [1518-11-01 00:30] falls asleep
# [1518-11-01 00:55] wakes up
# [1518-11-01 23:58] Guard #99 begins shift
# [1518-11-02 00:40] falls asleep
# [1518-11-02 00:50] wakes up
# [1518-11-03 00:05] Guard #10 begins shift
# [1518-11-03 00:24] falls asleep
# [1518-11-03 00:29] wakes up
# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
# [1518-11-05 00:03] Guard #99 begins shift
# [1518-11-05 00:45] falls asleep
# [1518-11-05 00:55] wakes up