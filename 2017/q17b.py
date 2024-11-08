class Node:
    def __init__(self, next=None, prev=None, data=None):
        # reference to next node in DLL
        self.next = next if next is not None else self
        # reference to previous node in DLL
        self.prev = prev if next is not None else self
        self.data = data


steps = 354

value_after_zero = -1

size = 1

current = 0

for _ in range(50000000):
    current = (current + steps) % size
    if current == 0:
        value_after_zero = size
    current += 1
    size += 1

print(value_after_zero)


# 2017x is data achter 0 1889 (354), 0 1226 (3)


