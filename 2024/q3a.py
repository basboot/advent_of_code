import re

file1 = open('q3a.txt', 'r')
line: str = "-".join(file1.readlines())

def multiply(line):

    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line)

    print(matches)

    return sum([int(x) * int(y) for (x, y) in matches])

enabled = True
result = ""

while True:
    print(enabled)
    i = line.find("don't()" if enabled else "do()")
    print(enabled, i, line)

    if enabled:
        if i == -1:
            result += line
        else:
            result += line[0:i]

    line = line[i + 7 if enabled else i + 4:]

    print("result", result)

    enabled = not enabled

    if i == -1:
        break


    # shorten line
print(">>> ", result)
print(multiply(result))
