from tools.advent_tools import *

file1 = open('q20a.txt', 'r')
file_lines = file1.readlines()

algorithm, _, _ = read_grid(file_lines[0], GRID_SET, f_prepare_line=lambda a: a.rstrip(), value_conversions={"#": True, ".": False}, int_conversion=False)
image, width, height = read_grid(file_lines[2:], GRID_SET, f_prepare_line=lambda a: a.rstrip(), value_conversions={"#": True, ".": False}, int_conversion=False)

print(algorithm)
print(image)

def get_extrema(image):
    image_points = np.array(list(image))
    i_min = min(image_points[:, 0])
    i_max = max(image_points[:, 0])
    j_min = min(image_points[:, 1])
    j_max = max(image_points[:, 1])
    return i_min, i_max, j_min, j_max



outside = False # default uit buiten image

def get3x3(center, image, i_min, i_max, j_min, j_max, outside):
    result = 0
    ci, cj = center
    for i in [-1, 0, 1]: # TODO: check order
        for j in [-1, 0, 1]:
            result <<= 1 # shift left

            # inside (add 1 if in image)
            if (ci + i, cj + j) in image:
                result |= 1 # add 1

            # outside (add 1 if outside is True)
            if outside and (ci + i < i_min or ci + i > i_max or cj + j < j_min or cj + j > j_max):
                result |= 1  # add 1

    return result

def apply_algorithm(image, algorithm, outside):
    i_min, i_max, j_min, j_max = get_extrema(image)

    convolution = set()
    for i in range(i_min - 1, i_max + 2):
        for j in range(j_min - 1, j_max + 2):
            value = get3x3((i, j), image, i_min, i_max, j_min, j_max, outside)

            if (value, 0) in algorithm:
                convolution.add((i, j))

    outside = (0b111111111 if outside else 0, 0) in algorithm
    return convolution, outside

print(outside)

print(len(image), outside)

for i in range(50):
    image, outside = apply_algorithm(image, algorithm, outside)
    print(len(image), outside)


