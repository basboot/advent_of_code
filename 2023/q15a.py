# Using readlines()
file1 = open('q15a.txt', 'r')
lines = file1.readlines()

# helper function for debugging
def show_boxes():
    for b in range(len(boxes)):
        box = boxes[b]
        for i in range(len(box)):
            print(f"box {b}: {i + 1}{box[i]}")

# hash algo
def hash(input, start=0):
    if len(input) == 0:
        return start

    return hash (input[1:], ((start + ord(input[0])) * 17) % 256)

# create 256 empty boxes
boxes = [[] for _ in range(256)]

# find index of (lens, focus) in box (or None)
def find_lens(lens, box):
    for i in (i for i, (l, f) in enumerate(box) if l == lens):
        return i # just return first
    return None


for operation in lines[0].split(","):
    command = operation.split("=")

    focus = None
    if len(command) == 2: # =
        # insert or replace
        lens, focus = command
        box = hash(lens)
        i = find_lens(lens, boxes[box])
        if i is not None:
            boxes[box][i] = (lens, int(focus))
        else:
            boxes[box].append((lens, int(focus)))

    else: #-
        # go to the relevant box and remove the lens with the given label if it is present in the box
        lens = command[0][:-1] # remove - from box id
        box = hash(lens)
        i = find_lens(lens, boxes[box])
        if i is not None:
            boxes[box].pop(i)

    # show_boxes()

# calc total focal
total = 0
for b in range(len(boxes)):
    box = boxes[b]
    for i in range(len(box)):
        _, focus = box[i]
        total = total + (b + 1) * (i + 1) * focus

print("Part 1", sum([hash(h) for h in lines[0].split(",")]))

print("Part 2", total)