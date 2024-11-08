from collections import Counter

file1 = open('q4a.txt', 'r')
lines = file1.readlines()


def create_checksum(letters):
    letter_counts = sorted(list(letters.items()), key=lambda x: (-x[1], x[0]))
    letters_only = "".join([x for x, y in letter_counts])
    return letters_only[0:5]


total = 0

for line in lines:
    room, checksum = line.rstrip().replace("]", "").split("[")
    letters = Counter("".join(room.split("-")[0:-1]))
    id = int(room.split("-")[-1])

    if create_checksum(letters) == checksum:
        total += id

        # decrypt real rooms
        decrypted = []
        for word in room.split("-")[0:-1]:
            decrypted.append("".join([chr(((ord(x) - ord('a') + id) % 26) + ord('a')) for x in word]))

        print(" ".join(decrypted), id)


print("Part 1", total)