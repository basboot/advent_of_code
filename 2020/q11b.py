from tools.advent_tools import *

file1 = open('q11a.txt', 'r')
lines = file1.readlines()

# create all nodes


empty_seats, width, height = read_grid(lines, GRID_SET, f_prepare_line=lambda x: x.rstrip(),
                                       value_conversions={"L": True, ".": False}, int_conversion=False)


print(width, height)
print(empty_seats)
print(len(empty_seats))

occupied_seats = set() # all seats start empty

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

def show_seats():
    for i in range(height):
        for j in range(width):
            if (i, j) in empty_seats:
                print("L", end="")
            else:
                if (i, j) in occupied_seats:
                    print("#", end="")
                else:
                    print(".", end="")
        print()


def count_neighbours(seat, seats, empty_seats, max_len=width):
    i, j = seat

    neighbours = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue # skip self

            for n in range(1, max_len + 1):
                ni, nj = i + di * n, j + dj * n
                if ni < 0 or ni > height or nj < 0 or nj > width: # don't look beyond the map
                    break
                if (ni, nj) in empty_seats: # first visible seat is empty, do not count neighbours for direction
                    break
                if (ni, nj) in seats:  # first visible seat is occupied, do not count extra neighbours for direction
                    neighbours += 1
                    break
    return neighbours

def iterate(empty_seats, occupied_seats):
    next_empty_seats = set()
    next_occupied_seats = set()

    for seat in empty_seats: # If a seat is empty (L)
        if count_neighbours(seat, occupied_seats, empty_seats) == 0: # and there are no occupied seats adjacent to it
            next_occupied_seats.add(seat) # the seat becomes occupied.
        else:
            next_empty_seats.add(seat) # Otherwise, the seat's state does not change.

    for seat in occupied_seats: # If a seat is occupied (#)
        if count_neighbours(seat, occupied_seats, empty_seats) > 4: # and FIVE or more seats adjacent to it are also occupied
            next_empty_seats.add(seat) # the seat becomes empty
        else:
            next_occupied_seats.add(seat) # Otherwise, the seat's state does not change

    return (next_empty_seats, next_occupied_seats,
            empty_seats == next_empty_seats and occupied_seats == next_occupied_seats)


# show_seats()

while True:
    empty_seats, occupied_seats, no_changes = iterate(empty_seats, occupied_seats)

    # print("-----")
    # print(">", count_neighbours((0, 0), occupied_seats, empty_seats))
    # show_seats()
    if no_changes:
        break


print("Part 2", len(occupied_seats))

# empty_seats = set()
# empty_seats.add((0, 1))
# occupied_seats.add((0, 2))
# empty_seats.add((2, 0))
# occupied_seats.add((4, 0))
# empty_seats.add((2, 2))
# occupied_seats.add((4, 4))

print(">", count_neighbours((0, 0), occupied_seats, empty_seats))