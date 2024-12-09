from itertools import chain

import numpy as np

file1 = open('q9a.txt', 'r')
line = file1.readlines()[0].rstrip() + "0" # add zero for missing empty spot at end

disk = list(chain(*[[(i, int(files_free[0])), (-1, int(files_free[1]))] for i, files_free in enumerate(zip(line[0::2], line[1::2]))]))

def find_space(file_to_move):
    file_content, file_size = disk[file_to_move]

    # check disk left to right
    for i, disk_space in enumerate(disk):
        # no fit if past the file
        if i >= file_to_move:
            return None

        disk_content, disk_size = disk_space
        # space needs to be empty
        if disk_content > -1:
            continue
        # space needs to be large enough
        if disk_size < file_size:
            continue

        # found space!
        return i
    return None


# check files from right to left, so start with last
file_to_move_position = len(disk) - 1

while file_to_move_position > 0:
    file_content, file_size = disk[file_to_move_position]
    if file_content > -1:
        free_space_position = find_space(file_to_move_position)

        if free_space_position is not None:
            _, free_size = disk[free_space_position]
            next_content, next_size = disk[free_space_position + 1]

            # replace moved file with empty (we go back to forth, so we do not have to combine empty spaces)
            disk[file_to_move_position] = (-1, file_size)

            disk_after_move = disk[0:free_space_position] + [(file_content, file_size)]

            remaining = free_size - file_size
            if next_content == -1:
                # size not changed
                disk_after_move.append((-1, remaining + next_size))
                disk_after_move += disk[free_space_position + 2:]
            else:
                if remaining > 0:
                    disk_after_move.append((-1, remaining))
                    disk_after_move += disk[free_space_position + 1:]
                    # size increased by one
                    file_to_move_position += 1
                else:
                    # size not changed
                    disk_after_move += disk[free_space_position + 1:]

            disk = disk_after_move

    file_to_move_position -= 1

new_disk = list(chain(*[[file_content] * file_size for file_content, file_size in disk]))

print(f"Part 2, {np.sum((np.array(new_disk) * np.array(range(len(new_disk))))[np.array(new_disk) > 0])}")
