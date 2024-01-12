file1 = open('q10a.txt', 'r')
file_lines = file1.readlines()

pairs = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

incomplete_points = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

def analyze_chunks(chuncks):
    stack = []
    for chunk in chuncks:
        if chunk not in pairs:
            stack.append(chunk)
        else:
            last_chunck = stack.pop()
            if last_chunck != pairs[chunk]: # closed incorrect
                return error_points[chunk], []
    # not corrupted (but might be incomplete)
    return 0, stack


def incomplete_score(incomplete_chuncks):
    score = 0
    while(len(incomplete_chuncks) > 0):
        chunk = incomplete_chuncks.pop()
        points = incomplete_points[chunk]

        score *= 5
        score += points
    return score

total = 0

scores = []
for line in file_lines:
    chunks = list(line.rstrip())
    corrupted_score, incomplete_cunks = analyze_chunks(chunks)
    total += corrupted_score

    if len(incomplete_cunks) > 0:
        scores.append(incomplete_score(incomplete_cunks))

print("Part 1", total)

scores.sort()

print("Part 2", scores[len(scores) // 2])

