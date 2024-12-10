from collections import defaultdict

file1 = open('q10a.txt', 'r')
lines = file1.readlines()

number_to_positions = defaultdict(list)
position_to_number = {}

for i, row in enumerate(lines):
    for j, n in enumerate(map(int, list(row.rstrip()))):
        position_to_number[(i, j)] = n
        number_to_positions[n].append((i, j))

reachable_nines = defaultdict(set)
n_paths_to_nines = defaultdict(int)


# set end height values at 9
for position in number_to_positions[9]:
    reachable_nines[position].add(position)
    n_paths_to_nines[position] = 1

# update height values from 8 to 0
for height in range(9, 0, -1):
    for position in number_to_positions[height]:
        i, j = position
        reachable_nines_from_next = reachable_nines[position]
        n_paths_to_nines_from_next = n_paths_to_nines[position]
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if (ni, nj) in position_to_number and position_to_number[(ni, nj)] == height - 1:
                reachable_nines[(ni, nj)] = reachable_nines[(ni, nj)].union(reachable_nines_from_next)
                n_paths_to_nines[(ni, nj)] += n_paths_to_nines_from_next

print(f"Part 1, {sum([len(reachable_nines[position]) for position in number_to_positions[0]])}")
print(f"Part 2, {sum([n_paths_to_nines[position] for position in number_to_positions[0]])}")

