from collections import deque, defaultdict

file1 = open('q24a.txt', 'r')
lines = file1.readlines()

reading_inputs = True


message_queue = deque()
gates = []

inputs1 = defaultdict(list)
inputs2 = defaultdict(list)

for line in lines:
    row = line.rstrip()
    if row == "":
        reading_inputs = False
        continue

    if reading_inputs:
        destination, signal = row.split(": ")
        message_queue.append((destination, int(signal)))
    else:
        input1, operation, input2, output = row.replace("-> ", "").split(" ")

        gates.append([None, None, operation, output])

        inputs1[input1].append(len(gates) - 1)
        inputs2[input2].append(len(gates) - 1)

IN1, IN2, OP, OUT = 0, 1, 2, 3

print(message_queue)

solution = []

while len(message_queue) > 0:
    destination, signal = message_queue.popleft()
    # print("S", destination, signal)

    if destination in inputs1:
        for gate in inputs1[destination]:
            assert gates[gate][IN1] is None, "gate already received signal 1"
            gates[gate][IN1] = signal

            if gates[gate][IN2] is not None:
                match gates[gate][OP]:
                    case "AND":
                        result = gates[gate][IN1] & gates[gate][IN2]
                    case "OR":
                        result = gates[gate][IN1] | gates[gate][IN2]
                    case "XOR":
                        result = gates[gate][IN1] ^ gates[gate][IN2]
                    case _:
                        assert False, "unknown op"
                message_queue.append((gates[gate][OUT], result))

    if destination in inputs2:
        for gate in inputs2[destination]:
            assert gates[gate][IN2] is None, "gate already received signal 2"
            gates[gate][IN2] = signal

            if gates[gate][IN1] is not None:
                match gates[gate][OP]:
                    case "AND":
                        result = gates[gate][IN1] & gates[gate][IN2]
                    case "OR":
                        result = gates[gate][IN1] | gates[gate][IN2]
                    case "XOR":
                        result = gates[gate][IN1] ^ gates[gate][IN2]
                    case _:
                        assert False, "unknown op"

                message_queue.append((gates[gate][OUT], result))

    if destination[0] == 'z':
        solution.append((destination, signal))

print(solution)

print(int("".join([str(x[1]) for x in sorted(solution, reverse=True)]), 2))
total = 0

print(f"Part 1, {total}")
