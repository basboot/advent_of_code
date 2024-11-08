from collections import Counter

file1 = open('q6a.txt', 'r')
lines = file1.readlines()

message_len = len(lines[0].rstrip())

characters = [""] * message_len

for line in lines:
    for i in range(message_len):
        characters[i] += line[i]

print("Part 1", "".join([Counter(x).most_common(1)[0][0] for x in characters]))

print("Part 2", "".join([list(reversed(Counter(x).most_common()))[0][0] for x in characters]))
