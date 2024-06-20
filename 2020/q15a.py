file1 = open('q15a.txt', 'r')
lines = file1.readlines()

spoken_numbers = {}

def last_spoken(number, turn):
    global spoken_numbers
    lp = 0
    if number in spoken_numbers:
        lp = turn - spoken_numbers[number]
    spoken_numbers[number] = turn

    return lp


init_spoken = [int(x) for x in lines[0].rstrip().split(",")]

last_number = 0

i = 0
for i in range(len(init_spoken)):
    print(last_spoken(init_spoken[i], i))
    last_number = init_spoken[i]

# i += 1

while i < 30000000 - 1:
    last_number = last_spoken(last_number, i)
    i += 1

print(last_number)