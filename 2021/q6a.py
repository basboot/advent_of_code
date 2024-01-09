file1 = open('q6a.txt', 'r')
file_lines = file1.readlines()

fish_list = [int(x) for x in file_lines[0].rstrip().split(",")]

fish = [0] * 9 # 0 to 8

for f in fish_list:
    fish[f] += 1

DAYS = 256

for i in range(DAYS):
    # day 0 to day 6 and 8
    day0 = fish.pop(0)
    fish[6] += day0
    fish.append(day0)

print(sum(fish))