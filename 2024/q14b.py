import math

import numpy as np
import pygame
from pygame.examples.cursors import image

file1 = open('q14a.txt', 'r')
lines = file1.readlines()

WIDTH = 101 # wide
HEIGHT = 103 # tall

robots = []
for line in lines:
    row = list(map(int, line.rstrip().replace("p=", "").replace(" v=", ",").split(",")))
    robots.append(row)

robots = np.array(robots)

lowest_std = math.inf

def update_robots(n):
    global lowest_std
    robots[:, 0] = np.mod(robots[:, 0] + n * robots[:, 2], WIDTH)
    robots[:, 1] = np.mod(robots[:, 1] + n * robots[:, 3], HEIGHT)

    image = np.zeros((HEIGHT, WIDTH))
    image[robots[:, 1], robots[:, 0]] = 1

    std = np.std(robots[:, 0]) + np.std(robots[:, 1])

    if std < lowest_std:
        lowest_std = std
        print("lower", std, "at", (seconds + 1))

    return image

def draw_robots(robots, surface, pixel_size):
    for y, row in enumerate(robots):
        for x, cell in enumerate(row):
            color = white if cell == 1 else black
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(surface, color, rect)

pygame.init()

PIXEL_SIZE = 5

screen_width, screen_height = WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Find Easter egg")

white = (255, 255, 255)
black = (0, 0, 0)

seconds = 0
image = update_robots(seconds)

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

running = True
auto = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                auto = True
            if event.key == pygame.K_DOWN:
                auto = False

            if event.key == pygame.K_LEFT:
                image = update_robots(-1)
                seconds -= 1
            if event.key == pygame.K_RIGHT:
                image = update_robots(1)
                seconds += 1

    if auto:
        image = update_robots(1)
        seconds += 1

    screen.fill(black)

    draw_robots(image, screen, PIXEL_SIZE)

    text_surface = font.render(str(seconds), True, (0, 255, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()

    clock.tick(30)

# Quit Pygame
pygame.quit()

# 500 robots

# net boven 10000 zijn we uiteraard rond

# 72 hor 93 ver