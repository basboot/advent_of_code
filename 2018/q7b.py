file1 = open('q7a.txt', 'r')

EXTRA_TIME = 60
MAX_WORKERS = 5

steps = {}

for line in file1:
    first_step, next_step = line.rstrip().replace("Step ", "").replace(" can begin.", "").split(" must be finished before step ")
    if first_step not in steps:
        steps[first_step] = { "constraints": set(), "time_left": EXTRA_TIME + ord(first_step) - ord('A') + 1 }
    if next_step not in steps:
        steps[next_step] = { "constraints": set(), "time_left": EXTRA_TIME + ord(next_step) - ord('A') + 1 }

    steps[next_step]["constraints"].add(first_step)

def get_next(workers):
    next_steps = list(filter(lambda x: x not in workers, sorted(list(steps.keys()), key=lambda k: (len(steps[k]["constraints"]), k))))

    if len(next_steps) == 0:
        return None # no more steps left
    else:
        if len(steps[next_steps[0]]["constraints"]) == 0:
            return next_steps[0]
        else:
            return None # no unconstraint steps left


def remove_constraint(step):
    for key in steps:
        if step in steps[key]["constraints"]:
            steps[key]["constraints"].remove(step)

workers = []

t = 0
while len(steps) > 0:
    print("time", t)
    # TODO: not very efficient to call get+next two times
    # start working if a worker is free, a step is not constraint, and is not being worked on already
    while len(workers) < MAX_WORKERS and get_next(workers) is not None:
        step = get_next(workers)
        workers.append(step)
        print("start working", step)

    t += 1

    steps_to_remove = []
    for worker in workers:
        steps[worker]["time_left"] -= 1
        if steps[worker]["time_left"] == 0:
            steps_to_remove.append(worker)

    for step in steps_to_remove:
        remove_constraint(step)
        print("remove ", step)
        del steps[step]
        workers.remove(step) # free worker





print("Done, time is", t)

# 255 too low
# 1055 too high