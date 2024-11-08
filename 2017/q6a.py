file1 = open('q6a.txt', 'r')
lines = file1.readlines()

memory = [int(x) for x in lines[0].rstrip().split("\t")]
print(memory)


def redistribute(memory):
    index_max = max(range(len(memory)), key=memory.__getitem__)

    value = memory[index_max] # save value
    memory[index_max] = 0 # reset mem

    # redist over next
    for i in range(value):
        memory[(index_max + i + 1) % len(memory)] += 1

    return memory


distributions = {tuple(memory): 0}
cycles = 0
while True:
    cycles += 1
    memory = redistribute(memory)

    if tuple(memory) in distributions:
        print("Found loop size", cycles - distributions[tuple(memory)])

        break
    else:
        distributions[tuple(memory)] = cycles

print("Part 1", cycles)





