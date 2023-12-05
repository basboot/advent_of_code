# Using readlines()
file1 = open('q10a.txt', 'r')
lines = file1.readlines()

x = 1
cycle = 0

strength = 0

screen = list("." * 240)

def clock_inc():
    global cycle
    global strength
    global screen
    cycle += 1

    # print(f"cycle {cycle}, x = {x}")

    if (cycle - 20) % 40 == 0:
        print(f"cycle {cycle}, x = {x}, strength = {cycle * x}")
        strength += cycle * x

    pixel = ((cycle - 1) % 40) + 1
    print(pixel, (cycle - 1) % 40, cycle - 1)
    # update screen
    print(f"cycle {cycle}, x = {x} => [{x - 1}, {x + 1}]")
    if x  == pixel or x + 1 == pixel or x + 2 == pixel:
        screen[cycle - 1] = "#"
    print("".join(screen[0:40]))

for line in lines:
    row = line.rstrip()
    # print("input: ", row)

    if len(row.split(" ")) > 1:
        command, argument = row.split(" ")
    else:
        command = row

    match command:
        case "noop":
            clock_inc()
        case "addx":
            clock_inc()
            clock_inc()
            x += int(argument)


print(strength)

for i in range(0, 240, 40):
    print("".join(screen[i:i+40]))