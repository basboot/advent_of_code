import re

from tools.piece import *
from tools.puzzle import Puzzle

import sys
sys.setrecursionlimit(20000)

def parse_file(filepath):
    blocks = {}
    dimensions_data = []
    n_blocks_data = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()

    current_block_id = None
    current_block_coords = []
    row_index = 0

    for line in lines:
        line = line.strip()

        # Check for a new block definition (e.g., "0:")
        block_match = re.match(r'^(\d+):$', line)
        if block_match:
            # If we were processing a previous block, save it first
            if current_block_id is not None:
                blocks[current_block_id] = current_block_coords
            
            # Start a new block
            current_block_id = int(block_match.group(1))
            current_block_coords = []
            row_index = 0
            continue

        # Check for a dimension line (e.g., "4x4: ...")
        dimension_match = re.match(r'^(\d+)x(\d+):\s*(.*)$', line)
        if dimension_match:
            # If we were processing a block, save it before moving on
            if current_block_id is not None:
                blocks[current_block_id] = current_block_coords
                current_block_id = None # Stop block processing

            width = int(dimension_match.group(1))
            height = int(dimension_match.group(2))
            numbers = list(map(int, dimension_match.group(3).split()))
            
            dimensions_data.append(((width, height), numbers))
            n_blocks_data.append(numbers)
            continue

        # If we are inside a block, process its content
        if current_block_id is not None and line:
            for col_index, char in enumerate(line):
                if char == '#':
                    # Create coordinates as (i, j) which is (row, col)
                    current_block_coords.append((row_index, col_index))
            row_index += 1

#[(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    # Save the last block if the file ends with it
    if current_block_id is not None:
        blocks[current_block_id] = current_block_coords

    return blocks, dimensions_data

if __name__ == "__main__":
    blocks, trees_and_presents = parse_file('q12a.txt')

    # puzzle_pieces = [
    #     create_piece([(0, 0)], 'A'),
    #     create_piece([(0, 0), (1, 0), (1, 1)], 'B'),
    #     create_piece([(10, 1), (10, 2), (10, 3), (9, 3)], 'C')
    # ]
    #
    # p = Puzzle(3, 3, puzzle_pieces)
    #
    # # p.invalidate((0, 0))
    #
    # s = p.solve(all_solutions=True)
    # print(s)
    # for i in range(len(s)):
    #     print(f"Solution #{i}")
    #     p.solution = s[i]
    #     print(p)

    total = 0
    id = 0
    for (width, height), presents in trees_and_presents:

        # fits without overlap, no need to analyze
        if (width // 3) * (height // 3) >= sum(presents):
            total += 1
            continue

        id += 1
        pieces = []
        n_blocks = 0
        for present_id, amount in enumerate(presents):
            n_blocks += len(blocks[present_id]) * amount
            for i in range(amount):
                # print(blocks[present_id])
                pieces.append(create_piece(blocks[present_id], chr(present_id + ord('A'))))

        # more blocks than space will never fit, no need to analyze
        if n_blocks > width * height:
            continue

        # print(len(pieces))
        # print(pieces)

        print(">> Need to analyze: ", width, height)

        p = Puzzle(width, height, pieces) # order w x h should not matter

        print("max empty", p.max_empty)
        print("solution")
        solution = p.solve()
        if len(solution) > 0:
            total += 1

    print(f"Part 1: {total}")
