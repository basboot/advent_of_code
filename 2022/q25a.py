# Using readlines()
file1 = open('q25a.txt', 'r')
lines = file1.readlines()

snafu_to_dec = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

def base5(d):
    if d == 0:
        return [0]

    result = []
    while d > 0:
        result.append(d % 5)
        d = d // 5

    result.reverse()

    return result

def convert_to_dec(s):
    result = 0
    for i in range(len(s)):
        result += 5**(len(s) - 1 - i) * snafu_to_dec[s[i]]

    return result

def convert_to_snafu(d):
    b5 = base5(d)

    print(b5) # 1120411044030_5

    b5.reverse()

    result = []

    for i in range(len(b5)):
        if b5[i] > 2:
            if b5[i] == 5:
                result.append('0')
            else:
                result.append('=' if b5[i] == 3 else '-')
            # carry
            if i < len(b5) - 1:
                b5[i + 1] += 1
            else:
                result.append('1')
        else:
            result.append(str(b5[i]))

    result.reverse()
    return "".join(result)


total = 0
for line in lines:
    snafu = line.strip()
    print(convert_to_dec(snafu))
    total += convert_to_dec(snafu)

print(total)
print(convert_to_snafu(total))

# print(convert_to_dec('2-=')) # 1747
# print(base5(131))
#
# print(convert_to_snafu(314159265)) # 1121-1110-1=0


