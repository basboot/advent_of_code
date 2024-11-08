class Node:
    def __init__(self, next=None, prev=None, data=None):
        # reference to next node in DLL
        self.next = next if next is not None else self
        # reference to previous node in DLL
        self.prev = prev if next is not None else self
        self.data = data


steps = 354

current = Node(data=0)

value = 1

for _ in range(2017):
    for i in range(steps):
        current = current.next

    new_node = Node(current.next, current, value)
    current.next = new_node
    current = new_node
    value += 1

print("Part 1", current.next.data)



