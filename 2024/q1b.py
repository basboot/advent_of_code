from collections import Counter

import numpy as np
import numpy.typing as npt

# read and align lists (sort columns)
lists: npt.NDArray[int] = np.sort(np.loadtxt('q1a.txt', dtype=int), 0)

# count number frequencies in second list
counts: Counter = Counter(lists[:, 1])

# sum up product of all numbers in first list with their frequency in second list
total: int = sum([n * counts[n] for n in lists[:, 0]])


print(f"Part 2, similarity score = {total}")