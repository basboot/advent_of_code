# Using readlines()
import math

file1 = open('q7a.txt', 'r')
lines = file1.readlines()

root = {
    "name": "root",
    "parent": None,
    "files": [],
    "dirs": {},
    "size": 0
}
current_dir = root

total_size = 0

def update_size(dir, size):
    dir["size"] += size

    if dir["parent"] is not None:
        update_size(dir["parent"], size)

def find_max_size(dir, max_size):
    global total_size
    if dir["size"] < max_size:
        # print(dir["name"])
        total_size += dir["size"]

    for subdir in dir["dirs"]:
        find_max_size(dir["dirs"][subdir], max_size)

def find_closest_size(dir, min_size):
    # start at inf
    solution = math.inf

    # replace if this dir is large enough
    if dir["size"] > min_size:
        solution = dir["size"]

    for subdir in dir["dirs"]:
        # find solution for subdirs
        new_solution = find_closest_size(dir["dirs"][subdir], min_size)

        # udate if better
        solution = min(solution, new_solution)

    # return best solution
    return solution

for line in lines:
    row = line.rstrip()
    # print(current_dir)
    # print("input: ", row)

    assert len(row) > 0, "there should be no empty rows in the input"
    if row[0] == "$":
        # print("process command")

        command = row.split(" ")

        match command[1]:
            case "cd":
                match command[2]:
                    case "/":
                        current_dir = root
                    case "..":
                        assert current_dir["parent"] is not None, "cannot cd .. from root"
                        current_dir = current_dir["parent"]
                    case _:

                        if command[2] not in current_dir["dirs"]:
                            new_dir = {
                                "name": command[2],
                                "parent": current_dir,
                                "files": [],
                                "dirs": {},
                                "size": 0
                            }
                            current_dir["dirs"][command[2]] = new_dir

                        current_dir = current_dir["dirs"][command[2]]
            case "ls":
                pass

    else:
        # print("listing")
        listing = row.split(" ")
        if listing[0] == "dir":
            # ignore dirs
            pass
        else:
            current_dir["files"].append((int(listing[0]), listing[1]))
            update_size(current_dir, int(listing[0]))


print(root["size"])

find_max_size(root, 100000)

# 7a
print(total_size)

#7b
disk_size = 70000000
needed_space = 30000000
free_space = disk_size - root["size"]
minimal_free_up = needed_space - free_space

print(f"need to free up {minimal_free_up}")

print(find_closest_size(root, minimal_free_up))