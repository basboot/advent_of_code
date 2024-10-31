# naive

start = [3,1,1,3,3,2,2,1,1,3] # conway 83 Bi
sequence = start

def get_first(numbers):
    if len(numbers) == 0:
        return None, None, None
    n = numbers[0]
    count = 0
    while count < len(numbers) and numbers[count] == n:
        count += 1

    return n, count, numbers[count:]

for i in range(40):
    print(i)
    next_sequence = []
    while True:
        n, count, sequence = get_first(sequence)
        if n is None:
            break
        next_sequence += [count, n]
    sequence = next_sequence

print(len(sequence))

# conway = 1.30357726903429639125709911215255189073070250465940487575486139062855088785246155712681576686442522555
#
# print(10 * conway ** 49)


# 329356

# 4382301 too low