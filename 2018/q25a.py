from scipy.spatial.distance import cityblock

file1 = open('q25a.txt', 'r')
lines = file1.readlines()

points = []
constellations = {}
n_constellations = 0

for line in lines:
    x, y, z, r = [int(x) for x in line.rstrip().split(",")]
    constellations[n_constellations] = [(x, y, z, r)]
    n_constellations += 1

print(constellations)

change = True
while change:
    constellation_list = list(constellations.keys())
    print(len(constellation_list))

    change = False
    for constellation in constellation_list:
        constellation_positions = constellations[constellation]

        for other_constellation in constellation_list:
            if constellation == other_constellation:
                continue # don't compare to self
            other_constellation_positions = constellations[other_constellation]

            for position in constellation_positions:
                for other_position in other_constellation_positions:
                    if cityblock(position, other_position) <= 3:
                        constellations[constellation] = constellations[constellation] + constellations[other_constellation]
                        del constellations[other_constellation]
                        change = True
                        break
                if change:
                    break
            if change:
                break
        if change:
            break


print(constellations)

print("Part 1", len(constellations))

# not efficient
# better: mark random, sort others on distance, mark all unmarked that are close, and recurse on them -- when done you found the first constellation








