file1 = open('q9a.txt', 'r')
lines = file1.readlines()

compressed = lines[0].rstrip()

# print(compressed)

def get_next_marker(input):
    start_marker = input.find("(")

    if start_marker < 0:
        return input, None, None, ""

    end_marker = input.find(")")
    length, repeats = [int(x) for x in input[start_marker + 1: end_marker].split("x")]
    decrypted = input[0:start_marker]

    return decrypted, input[end_marker + 1:end_marker + 1 + length], repeats, input[end_marker + 1 + length:]

uncompressed = ""

while len(compressed) > 0:
    processed, repeated_text, n_repeats, compressed = get_next_marker(compressed)
    uncompressed += processed
    if repeated_text is not None:
        uncompressed += n_repeats * repeated_text


print("Part 1", len(uncompressed))



