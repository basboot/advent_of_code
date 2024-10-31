import numpy as np


def spiral_pattern(n):
    """
    Generate a spiral pattern of coordinates.

    :param n: Number of coordinates to generate.
    :return: Generator yielding (x, y) coordinates in a spiral pattern.
    """
    position = 0 + 0j  # Starting at (0, 0)
    yield (position.real, position.imag)

    step_size = 1
    direction = 1 + 0j  # Initially moving to the right
    while n > 1:
        # Move in the current direction
        for _ in range(step_size):
            if n <= 1: return
            position += direction
            yield (position.real, position.imag)
            n -= 1

        # Rotate 90 degrees counterclockwise by multiplying by 1j
        direction *= 1j

        # Move in the current direction
        for _ in range(step_size):
            if n <= 1: return
            position += direction
            yield (position.real, position.imag)
            n -= 1

        # Rotate 90 degrees counterclockwise by multiplying by 1j
        direction *= 1j

        # Increase step size after completing a full turn (right + up or left + down)
        step_size += 1


offset = 50
memory = np.zeros((offset * 2, offset * 2), dtype=int)

max_value = 277678
value = 0
for pos in spiral_pattern(100):
    x, y = [int(i) + offset for i in pos]
    value = np.sum(memory[x - 1: x + 2, y - 1: y + 2])
    if value == 0:
        value = 1
    memory[x, y] = value
    print(value)
    if value > max_value:
        break

print(memory)