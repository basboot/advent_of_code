import numpy as np
from PIL import Image

file1 = open('q8a.txt', 'r')
lines = file1.readlines()

display_rows = 6
display_cols = 50

display = np.zeros((display_rows, display_cols))

for line in lines:
    action = line.rstrip().replace("x=", "").replace("y=", "").split(" ")

    # print(action)

    match action[0]:
        case "rect":
            cols, rows = [int(x) for x in action[1].split("x")]
            # print(cols, rows)
            display[0:rows,0:cols] = 1

        case "rotate":
            rowcol = int(action[2])
            shift = int(action[4])
            if action[1] == "row":
                display[rowcol, :] = np.roll(display[rowcol, :], shift)
            else:
                display[:, rowcol] = np.roll(display[:, rowcol], shift)




print("Part 1", np.sum(display))

im = Image.fromarray((1 - display) * 255)
im.show()

