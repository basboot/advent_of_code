# steeds 2x dezelfde lengte
# daarna 1 langer
# steeds 1 overlap
# init met down, 1, daarna start met 2 naar rechts
import math


# alle punten n, n hebben de waarde (2n - 1) ^ 2

# from number, identify  the 'depth'
# return coordinate of lower right coordinate, size of the 'ring', value of coordinate
def get_region(n):
    r = math.ceil((math.sqrt(n)))
    if r % 2 == 0:
        r += 1
    return (r // 2, r // 2), r, r ** 2


def get_position(n, start_pos, ring_size, start_n):
    current_n = start_n
    current_x, current_y = start_pos

    if current_n == n:
        return pos

    if n + ring_size > current_n:
        return current_x - (current_n - n), current_y
    else:
        current_x = current_x - ring_size + 1
        current_n = current_n - ring_size + 1

    if n + ring_size > current_n:
        return current_x, current_y - (current_n - n)
    else:
        current_y = current_y - ring_size + 1
        current_n = current_n - ring_size + 1

    if n + ring_size > current_n:
        return current_x + (current_n - n), current_y
    else:
        current_x = current_x + ring_size - 1
        current_n = current_n - ring_size + 1

    return current_x, current_y + (current_n - n)

n = 277678
pos, ring_size, start_n = get_region(n)

x, y = get_position(n, pos, ring_size, start_n)

print("Part 1", abs(x) + abs(y))

