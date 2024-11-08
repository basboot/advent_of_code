# Using readlines()
file1 = open('q20a.txt', 'r')
lines = file1.readlines()
from functools import reduce

from pyvis.network import Network


# modules
# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
# There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.
# Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the button module. When you push the button, a single low pulse is sent directly to the broadcaster module.


class Module:
    def __init__(self, name, type, outputs):
        self.inputs = {} # dict with mem for all inputs (conj)
        self.state = False # self state (flipflop) False=off
        self.outputs = outputs # list with other modules
        self.name = name
        self.type = type

    def init(self, modules):
        print(self.outputs)
        for output in self.outputs:
            modules[output].add_connection_from(name)

    def add_connection_from(self, module):
        self.inputs[module] = False # False is low

    def receive_signal(self, other_name, signal):
        response = None
        match self.type:
            case "%":
                if signal:
                    pass # If a flip-flop module receives a high pulse, it is ignored
                else:
                    # low pulse, it flips between on and off.
                    self.state = not self.state
                    # If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
                    response = self.state
            case "&":
                # When a pulse is received, the conjunction module first updates its memory for that input
                self.inputs[other_name] = signal
                # high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
                values = ([self.inputs[x] for x in self.inputs])
                response = not reduce(lambda a, b: a and b, values, True)

            case "broadcaster":
                response = signal
            case "button":
                response = False
            case "output":
                pass # for testing, does not send anytrhing
            case "rx":
                # print("RX: ", signal)
                if not signal:
                    print("FOUND")
                pass  # for testing, does not send anytrhing
            case _:
                assert True, "Unknown module"


        responses = []
        if response is not None:
            for output in self.outputs:
                responses.append((self.name, response, output))

        return responses

    def __repr__(self):
        return f"{self.type} module {self.name} connected to {self.outputs}, connections from {self.inputs}, state: {self.state}"

    def __str__(self):
        return f"{self.type} module {self.name} connected to {self.outputs}, connections from {self.inputs}, state: {self.state}"


modules = {}

# create graph to examine the network
net = Network(directed=True)
edges = []

for line in lines:
    row = line.rstrip().split(" -> ")

    if row[0] == "broadcaster":
        type = "broadcaster"
        name = "broadcaster"
    else:
        type = row[0][0]
        name = row[0][1:]

    connects_to = row[1].split(", ")

    print(type, name, connects_to)

    modules[name] = Module(name, type, connects_to)

    # nodes.append(f"{name}")

    # add node and label to graph network
    net.add_node(name, label=f"{name}-{type}")  # node id = 1 and label = Node 1

    # store edges in array, to connect them later
    for c in connects_to:
        edges.append((name, c))




# add button
modules["button"] = Module("button", "button", ["broadcaster"])
# add output
# modules["output"] = Module("output", "output", [])

# obsolete modules?
modules["rx"] = Module("rx", "rx", [])

# add edges to graph network
net.add_node("rx", label="RX")
for a, b in edges:
    net.add_edge(a, b)

# store graph in html file
net.show('q20b.html', notebook=False)

# analysis:
# RX only connected from qn wich is conj, so RX low will only happen is all inputs for qn are high
# qn connected from 4 isolated network parts (broadcast in -> ... -> single node -> qn
# monitoring the last single node for each network will hopefully lead to a solution

# easier -> just monitor messages to qn

for name in modules:
    modules[name].init(modules)


print(modules)

message_queue = []

n_high = 0
n_low = 0

monitoring = {
}
for presses in range(1000000000):

    if presses % 1000000 == 0:
        print(f">>>> PRESS BUTTON {presses}")
    message_queue += modules["button"].receive_signal("broadcaster", True) # value not important for button

    while len(message_queue) > 0:
        # print(message_queue)
        sender, signal, receiver = message_queue.pop(0)

        # monitor qn
        if receiver == "qn" and signal:
            if sender not in monitoring:
                monitoring[sender] = presses + 1

        # print(f"{sender} -{'high' if signal else 'low'}-> {receiver}")
        message_queue += modules[receiver].receive_signal(sender, signal)
    if len(monitoring) == 4:  # found all four
        break

print(monitoring)
intervals = ([monitoring[output] for output in monitoring])
# all primes so gcd is just the product
interval = reduce(lambda a, b: a * b, intervals, 1)
print(interval)

