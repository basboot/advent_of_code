file1 = open('q24a.txt', 'r')
lines = file1.readlines()

packets = []
for line in lines:
    packets.append(int(line.rstrip()))

packets.sort(reverse=True)
print(packets)

total_weight = sum(packets)
n_packets = len(packets)
assert total_weight % 3 == 0, "Total weight must be a multiple of 3"
target_weight = total_weight // 3

print("target", target_weight)

def get_next_packet(selected: int, current_packet: int, max_weight: int):
    while current_packet < n_packets:
        # not selected yet, and fits
        if (1 << current_packet & selected) == 0 and packets[current_packet] <= max_weight:
            yield current_packet
        current_packet += 1

best_n = n_packets

def get_packets(selected: int, current_packet: int, remaining_weight: int, n: int, first=False):
    global best_n

    if first and n > best_n:
        pass # break early if we cannot do better
    else:
        if remaining_weight == 0:
            if first:
                best_n = min(best_n, n)
            yield selected, n
        else:
            for selected_packet in get_next_packet(selected, current_packet, remaining_weight):
                yield from get_packets(selected | 1 << selected_packet, selected_packet + 1, remaining_weight - packets[selected_packet], n + 1, first)

results = []

for selected1, n1 in get_packets(0, 0, target_weight, 0, True):
    for selected2, n2 in get_packets(selected1, 0, target_weight, 0):
        for selected3, n3 in get_packets(selected2, 0, target_weight, 0):
            # analyse section 1
            q = 1
            for i in range(n_packets):
                if selected1 & 1 << i:
                    q *= packets[i]
            results.append((n1, q))
            break # only interested in first
        break

results.sort()
print("Part 1", results[0])

