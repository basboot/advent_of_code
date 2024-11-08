file1 = open('q20a.txt', 'r')

blacklist = []

for line in file1.readlines():
    start_ip, end_ip = [int(x) for x in line.rstrip().split("-")]
    blacklist.append((start_ip, end_ip))

max_ip = 4294967295 #
blacklist.append((max_ip + 1, max_ip + 1)) # end point for part 2

blacklist.sort()

last_blocked = -1
total_allowed = 0
lowest_found = False

for start_ip, end_ip in blacklist:
    if start_ip < last_blocked:
        last_blocked = max(last_blocked, end_ip)
        continue

    if start_ip > last_blocked + 1:
        if not lowest_found:
            print("Part 1", last_blocked + 1)
            lowest_found = True
        total_allowed += start_ip - last_blocked - 1
    last_blocked = end_ip


print("Part 2", total_allowed)

# 801988815 too high, check overlap
