# Using readlines()
import math
import queue
import sys

from tools.advent_tools import *

file1 = open('q18a.txt', 'r')
lines = file1.readlines()


digging, width, height = read_grid(lines, GRID_LIST, lambda a: a.strip().replace("(","").replace(")","").replace("#","").split(" "))

print(digging)


DIR_TO_WIND = {
    "3": NORTH,
    "0": EAST,
    "1": SOUTH,
    "2" : WEST
}

# Part A for testing
# DIR_TO_WIND = {
#     "U": NORTH,
#     "R": EAST,
#     "D": SOUTH,
#     "L" : WEST
# }

pos = (0, 0)
hole = []
lengths = []
for dig in digging:
    _, _, color = dig

    # print(color)
    direction = color[-1:]
    length_hex = color[:-1]

    length = int(length_hex, 16)

    lengths.append(length)

    i, j = pos
    di, dj = DIRECTIONS[DIR_TO_WIND[direction]]
    i = i + di * length
    j = j + dj * length
    pos = (i, j)

    hole.append(pos)

# PART A for tsting
# pos = (0, 0)
# hole = []
# for dig in digging:
#     direction, length, color = dig
#
#     i, j = pos
#     di, dj = DIRECTIONS[DIR_TO_WIND[direction]]
#     i = i + di * int(length)
#     j = j + dj * int(length)
#     pos = (i, j)
#
#     hole.append(pos)
#
# print(hole)


# first pos first to get all turning points left to right, top to bottom
hole.sort(key=lambda pos: ((pos[0] + 2**20) << 20) + (pos[1] + 2**20) << 0)

active_intervals = []

# calculate the number of blocks within all intervals
def sum_intervals(intervals):
    result = 0
    for i in range(0, len(intervals), 2):
        result += (intervals[i + 1] - intervals[i]) + 1 # +1 is ok
    return result


total = 0
current_scanwidth = 0 # start at 0
last_scanline_height = -math.inf # start with smallest

# find all intervals for the next scanline, combine them to get the new width, and also
# count the subtractions because they have to be added (boundaries have volume)
def calculate_next_scanwidth(start_i, start_intervals, hole):
    assert start_i < len(hole), "No scanline after end of digging"

    new_intervals = start_intervals.copy()

    i = start_i
    scanline_height = hole[i][0]
    scanline_width = sum_intervals(start_intervals)
    subtracted = 0

    while i < len(hole) and hole[i][0] == scanline_height:
        # print("From digging", hole[i], hole[i + 1])
        new_intervals.append(hole[i][1])
        new_intervals.append(hole[i + 1][1])
        new_intervals.sort()

        # remove doubles
        new_intervals_without_doubles = []
        j = 0
        while j < len(new_intervals) - 1:
            if new_intervals[j] == new_intervals[j+1]:
                j += 2 # skip
                continue
            new_intervals_without_doubles.append(new_intervals[j])
            j += 1
        if j == len(new_intervals) - 1: # last one is not a double
            new_intervals_without_doubles.append(new_intervals[j])

        # print(">>", new_intervals)
        # print("<<", new_intervals_without_doubles)
        new_intervals = new_intervals_without_doubles


        new_scanwidth = sum_intervals(new_intervals) # compare new width and increase subtracted if needed
        if new_scanwidth < scanline_width:
            subtracted += (scanline_width - new_scanwidth)
        scanline_width = new_scanwidth

        i += 2 # go to next
    return i, new_intervals, scanline_width, subtracted, scanline_height


i = 0
active_intervals = []
previous_width = 0
previous_height = 0
previous_sub = 0

while True:
    if i < len(hole):
        i, active_intervals, scanline_width, subtracted, scanline_height = calculate_next_scanwidth(i, active_intervals, hole)
        print(f"hoogte: {scanline_height}, breedte: {scanline_width}, (sub {subtracted})")
        print(active_intervals)

        # calc area between previous height and scanline - 1
        area = (scanline_height - previous_height) * previous_width

        total += area + subtracted # add area from previous part, add subtracted boundary for new part immedately
                                    # note that last line will only have a subtracted boundary and no width

        previous_height = scanline_height
        previous_width = scanline_width
    else:
        total += previous_sub # last line
        break


    # print(hole[i][0], hole[i+1][0])
    # assert hole[i][0] == hole[i+1][0], "scanline not horizontal!"
    #
    # active_intervals.append(hole[i][1])
    # active_intervals.append(hole[i + 1][1])
    # list(set(active_intervals)) # quick and dirty, remove doubles
    # active_intervals.sort()
    # current_scanwidth = sum_intervals(active_intervals)
    #
    # i += 2 # go to next interval




print(active_intervals)

print("Total", total)


# 952408144115
# 952408144115
# 952404152030
# 952406469534

# 952404941483, te weinig
# 952405550549
# 952405058904
# 952406127811
# 952410226786
# 952410109367


# # start empty
# active_intervals = []
#
#
# # add intervals from hole
#
# def merge_intervals(active_intervals, new_intervals):
#     active_start = True
#     new_start = True
#
#     merged_intervals = []
#
#     while len(active_intervals) > 0 or len(new_intervals) > 0:
#         # no more active, or active smallest
#         if len(active_intervals) == 0 or new_intervals[0] <= active_intervals[0]:
#             value = new_intervals.pop(0)
#             merged_intervals.append((value, new_start))
#             new_start = not new_start
#             continue
#
#         # no more new
#         if len(new_intervals) == 0 or active_intervals[0] < new_intervals[0]:
#             value = active_intervals.pop(0)
#             merged_intervals.append((value, active_start))
#
#             active_start = not active_start
#             continue
#
#     return merged_intervals
#
#
#
#
# # active_intervals, deleted = merge_intervals(active_intervals, [1, 10])
# #
# active_intervals, deleted = merge_intervals([1, 10], [5, 7])
# #
# # active_intervals, deleteds = merge_intervals(active_intervals, [10, 15])
#
# print(active_intervals, deleted)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#



# import math
# print(math.gcd(*lengths))

# print(len(hole))

# print(hole)

# active = []

# def add_scanline(active, left, right):
#     active_i = 0
#     new_active = []
#
#     # first find left
#     while active_i < len(active) and active[active_i] < left:
#         new_active.append(active[active_i])
#         active_i += 1
#
#     if active_i < len(active):
#         if active[active_i] == left:
#         # I think this means it cancels out
#             active_i += 1
#         else:
#             new_active.append(left)
#
#     while active_i < len(active) and active[active_i] < right:
#         new_active.append(active[active_i] - 1)
#         new_active.append(active[active_i])
#
#     if active_i < len(active):
#         if active[active_i] == right:
#             # cancel?
#             active_i += 1
#         else:
#             new_active.append(right)
#
#     while active_i < len(active):
#         new_active.append(active[active_i])
#         active_i += 1
#
#     # in the interval was not within rabge
#     if len(new_active) == 0 or new_active[-1] < left:
#         new_active.append(left)
#     if new_active[-1] < right:
#         new_active.append(right)
#
#     return new_active

# def add_scanline(active, left, right):
#     new_active = []
#     for i in range(0, len(active), 2):
#         start = active[i]
#         end = active[i + 1]
#
#         # outside new, so ignore
#         if end < left or start > right:
#             new_active.append(active[i])
#             new_active.append(active[i + 1])

# def add_scanline(active, left, right):
#     new_active = []
#     left_used = right_used = False
#     for act in active:
#         if act < left:
#             new_active.append(act)
#             continue # pass
#         if act > right:
#             if not left_used:
#                 left_used = True
#                 new_active.append(left)
#             if not right_used:
#                 right_used = True
#                 new_active.append(right)
#             new_active.append(act)
#             continue # pass
#         if act == left:
#             left_used= True
#             continue
#         if act == right:
#             right_used = True
#             continue # remove
#
#         if not left_used:
#             left_used = True
#             new_active.append(left)
#
#         # within bounds
#         new_active.append(act - 1)
#         new_active.append(act)
#
#
#     if not left_used:
#         new_active.append(left)
#     if not right_used:
#         new_active.append(right)
#     return new_active

# active = add_scanline(active, 10, 20)
# active = add_scanline(active, 1, 5)
# active = add_scanline(active, 22, 80)
# active = add_scanline(active, 5, 10)
# print(active)
# active = add_scanline(active, 15, 25)

#
# def process_new_boundaries(endpoints, processed, to_process, added, removed):
#     l, r = endpoints
#     # return modified
#     if len(to_process) == 0:
#         processed.append((l, r))
#         added += (r - l) + 1
#         return None, processed, to_process, added, removed
#
#     if r < to_process[0][0] - 1: # full interval smaller than active
#         processed = [(l, r)] + to_process
#         added += (r - l) + 1
#         return None, processed, [], added, removed
#
#     if l > to_process[-1][1] + 1: # full interval larger than active
#         processed = to_process + [(l, r)]
#         added += (r - l) + 1
#         return None, processed, [], added, removed
#
#     # item needs processing
#     l_active, r_active = to_process.pop(0) # remove item
#
#     # # connect to existing interval #TODO:
#     # if r == l_active: # connect
#     #     # processed = [(l, r_active)] + to_process
#     #     # added += (r - l) + 0 # TODO: check
#     #     added -= (r - l) # trick
#     #     return (l, r_active), processed, to_process, added, removed
#     # if r_active == l: # connect
#     #     processed = to_process + [(l_active, r)]
#     #     added += (r - l) + 0 # TODO: check
#     #     return None, processed, [], added, removed
#
#     # find overlap
#     if l < l_active: # keep first part and add it
#         processed = processed + [(l, l_active - 1)] # TODO: check
#         added += l_active - l # -1 already done?
#         return (l_active, r), processed, [(l_active, r_active)] + to_process, added, removed
#
#     # keep part of new interval possibly
#     if l > l_active:
#         processed = processed + [(l_active, l - 1)] # not new, no update of values
#         l_active = l # move left
#
#     # remove overlap from interval
#     if l == l_active:
#         if r >= r_active:
#             # cancel out
#             removed += (r_active - l)
#             if l == r:
#                 return None, processed + to_process, [], added, removed
#             else:
#                 return (r_active + 1, r), processed, to_process, added, removed
#         else:
#             # remove part
#             processed = processed + [(r, r_active)]
#             removed += (r - l_active)
#             return None, processed + to_process, [], added, removed
#
#
#
# def add_scanline(active, endpoints):
#     processed = []
#     to_process = active
#     added = 0
#     removed = 0
#
#     while endpoints is not None:
#         endpoints, processed, to_process, added, removed = process_new_boundaries(endpoints, processed, to_process, added, removed)
#         print(">", endpoints, processed, to_process, added, removed)
#
#     print(">>>", processed)
#
#     return processed
#
#
# active = add_scanline(active, (10, 20))
# active = add_scanline(active, (20, 21))
#
#
# # TODO: check corner cases + / - 1, and add + sub +-1
# # sub lijkt niet goed
#
#
#


    # else:
    #     # keep part of original
    #     processed = processed + [l_active - 1, l - 1]
    #
    # if r < r_active:
    #     # keep part of original
    #     processed = processed + [l_active - 1, l - 1]
    #
    # # TODO: remove middle part
    #
    #
    # l_part = max(l, l_active)
    # r_part = min(r, r_active)
    #
    #
    # if r >= r_active: # keep last part, and reprocess it
    #     pass



#
#
#
#
#
#
# exit()
#
#
# for i in range(0, len(hole), 2):
#     scanline_start = hole[i]
#     scanline_end = hole[i + 1]
#
#     assert scanline_start[0] == scanline_end[0], "scanline must be horizontal"
#
#     height, left, right = scanline_start[0], scanline_start[1], scanline_end[1]
#
#     print(left, right)
