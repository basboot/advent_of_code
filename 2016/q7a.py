from collections import Counter

file1 = open('q7a.txt', 'r')
lines = file1.readlines()

def has_abba(ip_part):
    if len(ip_part) < 4:
        return False

    for i in range(len(ip_part) - 3):
        if ip_part[i+0] == ip_part[i+3] and ip_part[i+1] == ip_part[i+2] and ip_part[i+0] != ip_part[i+1]:
            return True

    return False

def find_aba(ip_part):
    results = []
    if len(ip_part) < 3:
        return results

    for i in range(len(ip_part) - 2):
        if ip_part[i+0] == ip_part[i+2] and ip_part[i+0] != ip_part[i+1]:
            results.append(ip_part[i+1] + ip_part[i+2] + ip_part[i+1])

    return results # Note result is bab!

total = 0
total2 = 0

for line in lines:
    # read line
    ip_part = []
    abba_outside = False
    abba_inside = False
    aba_bab = False
    hypernets = []
    babs = []
    for c in list(line):
        match c:
            case "[":
                if has_abba(ip_part):
                    abba_outside = True
                babs += find_aba(ip_part)

                ip_part = []
            case "]":
                if has_abba(ip_part):
                    abba_inside = True
                hypernets.append("".join(ip_part))
                ip_part = []
            case "\n":
                if has_abba(ip_part):
                    abba_outside = True
                babs += find_aba(ip_part)
                ip_part = []
            case _:
                ip_part.append(c)

    # print(line.rstrip())
    # print(babs, hypernets)
    if abba_outside and not abba_inside:
        total += 1

    for bab in babs:
        for hypernet in hypernets:
            if hypernet.find(bab) > -1:
                aba_bab = True

    if aba_bab:
        total2 += 1


print("Part 1", total)
print("Part 2", total2)
