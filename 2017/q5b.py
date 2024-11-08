file1 = open('q5a.txt', 'r')
lines = file1.readlines()

jumps = []

for line in lines:
    jumps.append(int(line.rstrip()))

print(jumps)

ip = 0

steps = 0
while ip >= 0 and ip < len(jumps):
    line = jumps[ip]
    if jumps[ip] >= 3:
        jumps[ip] -= 1
    else:
        jumps[ip] += 1
    ip += line
    steps += 1

print("Part 2", steps)



