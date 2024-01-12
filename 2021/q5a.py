file1 = open('q5a.txt', 'r')
file_lines = file1.readlines()

lines = []
for file_line in file_lines:
    line = [tuple([int(x) for x in p.split(",")]) for p in file_line.rstrip().split(" -> ")]
    lines.append(line)

print(lines)

hor_lines = []
ver_lines = []

for line in lines:
    if line[0][0] == line[1][0]:
        # top to bottom
        if line[0][1] > line[1][1]:
            ver_lines.append([line[1], line[0]])
        else:
            ver_lines.append(line)
    if line[0][1] == line[1][1]:
        # always from left to right
        if line[0][0] > line[1][0]:
            hor_lines.append([line[1], line[0]])
        else:
            hor_lines.append(line)

    # ignore diagonals for part 1

print("ver", ver_lines)
print("hor", hor_lines)

# first remove overlapping horizontal lines (quick fix)
hor_lines.sort(key=lambda x: x[0][1])   # sorted by y, x?

# scan from top to bottom
ver_lines.sort(key=lambda x: x[0][1])   # sorted by top (=y of first)
hor_lines.sort(key=lambda x: x[0][1])   # sorted by y
active_lines = []                       # put vertical lines here when we find the top, will be sorted by bottom

# arrays contain lines, lines contain points and points comtain coordinates -> 3 layers!

total = 0
while len(hor_lines) > 0:
    # if ver line has top above y than next hor_line, make active (if there are still ver lines)
    if len(ver_lines) > 0 and ver_lines[0][0][1] < hor_lines[0][0][1]:
        active_lines.append(ver_lines.pop(0))
        active_lines.sort(key=lambda x: x[1][1]) # sort by bottom
        continue

    # if active line has bottom above next hor line, remove from active (if there is still an active line)
    if len(active_lines) > 0  and active_lines[0][1][1] < hor_lines[0][0][1]:
        active_lines.pop(0)
        continue

    # active and vert lines processed, so count the active lines that are crossed by the next hor line
    hor_line = hor_lines.pop(0)

    for line in active_lines:
        # line is crossed when its x value is in range of the hor line
        if line[0][0] >= hor_line[0][0] and line[0][0] <= hor_line[1][0]:
            total += 1

print(total)




