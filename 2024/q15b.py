import pygame
import sys

file1 = open('q15a.txt', 'r')
lines = file1.readlines()

GRID_SIZE = 10
DEBUG = True
FPS = 120

read_maze = True

walls = set()
boxes = set()

robot = 0
instructions = []

for i, line in enumerate(lines):
    row = line.rstrip()
    if row == "":
        read_maze = False
        continue

    if read_maze:
        for j, value in enumerate(list(row)):
            position = i + 2 * j * 1j
            match value.upper():
                case "#":
                    walls.add(position)
                case "O":
                    boxes.add(position)
                case "@":
                    robot = position

    else:
        instructions.extend(list(row))

total = 0

DIRECTIONS = {
    "<": -1j,
    "^": -1,
    ">": 1j,
    "v": 1
}

ROBOT, BOX = 0, 1

def show_warehouse(n):
    for i in range(n):
        skip_next = False
        for j in range(n * 2):
            if skip_next:
                skip_next = False
                continue

            position = i + 1j*j

            if position in boxes:
                print("[]", end="")
                skip_next = True
            else:
                if position in walls:
                    print("##", end="")
                    skip_next = True
                else:
                    if position == robot:
                        print("@", end="")
                    else:
                        print(".", end="")
        print()

def try_move(positions, direction):
    possible = True
    moves = set()
    for position in positions:
        if position in walls:
            possible = False
        if position in boxes:
            # try all possible positions where a box can be hit
            if direction in [1j, -1j]:
                next_positions = [position + direction * 2] # skip one place left/right because boxes have size 2
            else:
                # 3 options to hit a box up/down 1 left, same and 1 right
                next_positions = [position + direction + shift for shift in [direction * 1j, 0, direction * -1j]]

            new_possible, new_moves = try_move(next_positions, direction)
            # something can't move, nothing can move
            possible = possible and new_possible
            # if possible at this box to moves
            if possible:
                moves.add((position, position + direction))
            moves = moves.union(new_moves)
        if not possible :
            break
    return possible, moves

instruction_counter = 0

# update in function for animation
def next_instruction():
    global instruction_counter
    global robot

    # ready?
    if instruction_counter >= len(instructions):
        return False

    instruction = instructions[instruction_counter]

    # show_warehouse(10)
    direction = DIRECTIONS[instruction]

    # 4 different cases for robot, because robot is smaller than boxes
    if direction == -1j:
        next_positions = [robot + direction * 2]  # skip one place left
    else:
        if direction == 1j:
            next_positions = [robot + direction] # right is normal
        else:
            if direction == 1:
                # below + right (left = right ;-) # TODO: was makkelijker geweest als ik gewoon absoluut links had gebruikt
                next_positions = [robot + direction + shift for shift in [direction * -1j, 0]]
            else:
                next_positions = [robot + direction + shift for shift in [direction * 1j, 0]]  # above + left

    possible, moves = try_move(next_positions, direction)

    # only perform move if nothing is blocked
    if possible:
        for from_position, to_position in moves: # remove boxes that are going to move
            boxes.remove(from_position)
        for from_position, to_position in moves: # put them back
            boxes.add(to_position)
        robot = robot + direction # move robot

    instruction_counter += 1

    return instruction_counter < len(instructions)

def draw_square(screen, x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_box(screen, x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE * 2, GRID_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, GRID_SIZE * 2 - 4, GRID_SIZE - 4))

if DEBUG:
    pygame.init()

    # Screen dimensions
    screen_width, screen_height = 1000, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Day 15")

    clock = pygame.time.Clock()
    running = True

    ready = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ready = False # start

        screen.fill((0, 0, 0))

        draw_square(screen, robot.imag, robot.real, (255, 0, 0))
        for box in boxes:
            draw_box(screen, box.imag, box.real, (0, 255, 0))
        for wall in walls:
            draw_square(screen, wall.imag, wall.real, (0, 0, 255))
            draw_square(screen, wall.imag + 1, wall.real, (0, 0, 255))

        if not ready:
            ready = not next_instruction()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

while next_instruction():
    pass

# show_warehouse(10)
for box in boxes:
    total += box.imag + 100 * box.real

print(f"Part 1, {total}")

sys.exit()
