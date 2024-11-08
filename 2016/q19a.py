n_elves = 3004953

# even aantal, de even worden verwijderd
# oneven aantal, de even en nummer 1 worden verwijderd
# winnaar is nummer 1 + shifts van 2^round (omdat even sowieso verwijderd worden)

winner = 1

round = 0
while n_elves > 1:
    round += 1
    winner += (n_elves % 2) * 2**round
    n_elves //= 2



print("Part 1", winner)
