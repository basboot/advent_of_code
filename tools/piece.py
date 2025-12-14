import numpy as np
from dataclasses import dataclass, field

@dataclass
class Layout:
    blocks: list[tuple]

    def size(self):
        return len(self.blocks) + 1


@dataclass
class Piece:
    layouts: list[Layout]
    representation: str
    _max_width: int = field(init=False, repr=False, default=0)
    _max_height: int = field(init=False, repr=False, default=0)
    _min_width: int = field(init=False, repr=False, default=0)
    _min_height: int = field(init=False, repr=False, default=0)

    def __post_init__(self):
        """
        Calculates the min and max width/height across all layouts once after initialization.
        """
        if not self.layouts:
            return

        max_w, max_h = 0, 0
        min_w, min_h = float('inf'), float('inf')

        for layout in self.layouts:
            # The origin (0,0) is always part of the piece.
            all_x_coords = [b[0] for b in layout.blocks] + [0]
            all_y_coords = [b[1] for b in layout.blocks] + [0]

            # The width/height is the span from min to max coordinate.
            current_width = max(all_x_coords) - min(all_x_coords) + 1
            current_height = max(all_y_coords) - min(all_y_coords) + 1

            if current_width > max_w:
                max_w = current_width
            if current_height > max_h:
                max_h = current_height
            
            if current_width < min_w:
                min_w = current_width
            if current_height < min_h:
                min_h = current_height
        
        self._max_width = max_w
        self._max_height = max_h
        self._min_width = int(min_w)
        self._min_height = int(min_h)

    @property
    def max_width(self):
        """Returns the maximum width this piece can have in any orientation."""
        return self._max_width

    @property
    def max_height(self):
        """Returns the maximum height this piece can have in any orientation."""
        return self._max_height

    @property
    def min_width(self):
        """Returns the minimum width this piece can have in any orientation."""
        return self._min_width

    @property
    def min_height(self):
        """Returns the minimum height this piece can have in any orientation."""
        return self._min_height

    def size(self):
        return self.layouts[0].size()

# create a layout from a block_matrix by transforming the matrix to have the most left block
# on the top row as the origin
def create_layout(block_matrix):
    # get all rows where the y value is equal to the smallest y value (all blocks on the top row)
    result = np.where(block_matrix[:,1] == np.amin(block_matrix, axis=0)[1])

    # now store the smallest y found (= top row)
    smallest_y = block_matrix[result[0][0], 1]
    # and select the smallest x on the top row
    smallest_x = np.min(block_matrix[result[0], 0])

    new_matrix = block_matrix - np.array([smallest_x, smallest_y])

    points = []
    for row in new_matrix:
        point = tuple(row)
        if point != (0, 0):
            # print(tuple(row))
            points.append(tuple(row))
    # print(f"Layout({points})")

    return points

# blocks = all blocks!, origin does not have to be 0,0
def create_piece(blocks, name):

    # combine blocks to create matrix for easy rotation
    block_matrix = np.zeros((len(blocks), 2), dtype=np.int32)  # force ints
    for i in range(len(blocks)):
        block_matrix[i, :] = blocks[i]

    # create rotation and flip (mirror x) matrices
    rotate90 = np.array(((0, -1), (1, 0)))
    mirror_x = np.array(((-1, 0), (0, 1)))

    block_matrix_flipped = block_matrix @ mirror_x

    # print("%%%")
    # print(block_matrix)
    # print(block_matrix_flipped)

    # rotate normal and flipped blocks four times to create 8 layouts
    layouts = []
    used_layouts = set()  # store layouts in a set to detect duplicates
    for i in range(4):
        # print(f"rotate {i}")
        block_matrix = block_matrix @ rotate90
        block_matrix_flipped = block_matrix_flipped @ rotate90
        # print(block_matrix)
        # print(block_matrix_flipped)
        # print("LLLL")
        # print(create_layout(block_matrix))

        layout = create_layout(block_matrix)
        temp_layout_frozen_set = frozenset(layout)
        if temp_layout_frozen_set not in used_layouts:
            used_layouts.add(temp_layout_frozen_set)
            layouts.append(Layout(layout))
        #     print(f"+{ls}")
        # else:
        #     print(f"-{ls}")

        layout = create_layout(block_matrix_flipped)
        temp_layout_frozen_set = frozenset(layout)
        if temp_layout_frozen_set not in used_layouts:
            used_layouts.add(temp_layout_frozen_set)
            layouts.append(Layout(layout))
        #     print(f"+{ls}")
        # else:
        #     print(f"-{ls}")

        # print(used_layouts)
    p = Piece(layouts, name)
    # print(p)
    return p


if __name__ == '__main__':
    blocks = [(0, 0), (1, 0), (1, -1), (2, -1), (2, -2)]
    new_piece = create_piece(blocks, 'C')

    print("***")
    print(blocks)
    print(">>>")
    for layout in new_piece.layouts:
        print(layout)

    peters_puzzel_pieces = [
        # 0
        Piece([Layout([(1, -1), (1, 0), (1, 1), (1, 2)])], 'A'),
        # 1
        Piece([Layout([(1, 0), (0, 1), (1, 1), (0, 2)])], 'B'),
        # 2
        Piece([Layout([(1, 0), (1, -1), (2, -1)])], 'C'),
        # 3
        Piece([Layout([(0, 1), (0, 2), (1, 2), (2, 2)])], 'D'),
        # 4
        Piece([Layout([(1, 0), (1, -1), (1, 1), (2, 0)])], 'E'),
        # 5
        Piece([Layout([(1, 0), (1, 1), (1, 2), (0, 2)])], 'F'),
        # 6
        Piece([Layout([(1, 0), (1, -1), (2, -1), (0, 1)])], 'G'),
        # 7
        Piece([Layout([(1, 0), (1, -1), (1, 1)])], 'H'),
        # 8
        Piece([Layout([(0, 1), (1, 1), (2, 1)])], 'I'),
        # 9
        Piece([Layout([(1, 0), (1, -1), (2, 0), (2, 1)])], 'J')
    ]

    # for piece in peters_puzzel_pieces:
    #     print(piece)
    #     block_matrix = np.zeros((len(piece.layouts[0].blocks) + 1, 2), dtype=np.int32)
    #     for i in range(len(piece.layouts[0].blocks)):
    #         print(piece.layouts[0].blocks[i])
    #         block_matrix[i+1, :] = piece.layouts[0].blocks[i]
    #     print(block_matrix)
    #     rotate90 = np.array(((0, -1), (1, 0)))
    #     print(block_matrix @ rotate90)
    #     mirror_x = np.array(((-1, 0), (0, 1)))
    #     print(block_matrix @ mirror_x)
    #
    #     # find smallest x
    #     print("---")
    #     matrix = block_matrix @ mirror_x
    #
    #     print(np.amin(matrix, axis=0))
    #     result = np.where(matrix == np.amin(matrix))
    #     print(result)
    #
    #     # now find the smallest y in the results
    #     smalllest_x_pos = result[0]
    #     print(smalllest_x_pos)
    #     y_s = matrix[smalllest_x_pos, 1]
    #     print(y_s)
    #     smallest_y = np.min(y_s)
    #     print(smallest_y)
    #     smallest_x = matrix[smalllest_x_pos[0], 0]
    #     print(smallest_x)
    #
    #     print(matrix - np.array([smallest_x, smallest_y]))
    #
    #     new_matrix = matrix - np.array([smallest_x, smallest_y])
    #
    #     points = []
    #     for row in new_matrix:
    #         point = tuple(row)
    #         if point != (0, 0):
    #             print(tuple(row))
    #             points.append(tuple(row))
    #     print(f"Layout({points})")
    #
    #     # TODO: use offset to calc new layout (done)
    #     # TODO: don't forget to cast to int (done ;-)
    #     # TODO: print layouts (and remove 0,0)