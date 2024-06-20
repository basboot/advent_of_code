import math
from collections import Counter
from itertools import permutations
import numpy as np
from PIL import Image

file1 = open('q8a.txt', 'r')
lines = file1.readlines()

#25 pixels wide and 6 pixels tall

width = 25
height = 6

pixels = [int(x) for x in lines[0].rstrip()]

print(pixels)

layers = []

i = 0
min_layer = None
min_zeros = math.inf

image = [2] * width * height
while i < len(pixels):
    # if 2 in Counter(list(str(password))).values():
    layer = pixels[i:i + width * height]

    for j in range(width * height):
        if image[j] == 2:
            image[j] = layer[j]
    counter = Counter(pixels[i:i + width * height])
    if counter[0] < min_zeros:
        min_zeros = counter[0]
        min_layer = counter
    i += width * height

print("Part 1", min_layer[1] * min_layer[2])

# 0 black
# 1 white
im = Image.fromarray((np.array(image)).reshape((height, width)).astype('uint8') * 255)
im.show()

# 1656 too high