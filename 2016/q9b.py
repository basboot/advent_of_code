file1 = open('q9a.txt', 'r')
lines = file1.readlines()

compressed = lines[0].rstrip()

# print(compressed)

def get_next_marker(input_text):
    start_marker = input_text.find("(")

    if start_marker < 0:
        return len(input_text), None, None, ""

    end_marker = input_text.find(")")
    length, repeats = [int(x) for x in input_text[start_marker + 1: end_marker].split("x")]
    decrypted = input_text[0:start_marker]

    return len(decrypted), input_text[end_marker + 1:end_marker + 1 + length], repeats, input_text[end_marker + 1 + length:]


def uncompressed_length(compressed):
    uncompressed = 0

    while len(compressed) > 0:
        processed, repeated_text, n_repeats, compressed = get_next_marker(compressed)
        uncompressed += processed
        if repeated_text is not None:
            uncompressed += n_repeats * uncompressed_length(repeated_text)
    return uncompressed


print("Part 2", uncompressed_length(compressed))



