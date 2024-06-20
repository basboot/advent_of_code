file1 = open('q5a.txt', 'r')
lines = file1.readlines()

# FBFBBFFRLR

seats = []
for line in lines:
    row = line.rstrip().replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")

    seats.append(int(row, 2))

print("Part 1", max(seats))

seats.sort()

for i in range(2, len(seats)):
    if seats[i] > seats[i - 1] + 1:
        print("Part 2", seats[i - 1] + 1)
        exit()



