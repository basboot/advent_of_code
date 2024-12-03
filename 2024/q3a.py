import re

file1 = open('q3a.txt', 'r')
line: str = "-".join(file1.readlines()) # create single line (use separator to avoid creating a valid keyword)

def multiply(line: str) -> int:
    matches: [(str, str)] = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line)
    return sum([int(x) * int(y) for (x, y) in matches])

def strip_donts(line: str) -> str:
    enabled: bool = True
    result: str = ""

    while True:
        i: int = line.find("don't()" if enabled else "do()")

        # keep do's
        if enabled:
            result += line if i == -1 else line[0:i]

        # remove processed part
        line = line[i + 7 if enabled else i + 4:]

        enabled = not enabled

        # end of line
        if i == -1:
            break

    return result

print(f"Part 1 {multiply(line)}")
print(f"Part 2 {multiply(strip_donts(line))}")
