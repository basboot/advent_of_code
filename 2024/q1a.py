import numpy as np
import numpy.typing as npt

# read and align lists (sort columns)
lists: npt.NDArray[int] = np.sort(np.loadtxt('q1a.txt', dtype=int), 0)

# sum up distances between numbers in lists
total: int = np.sum(np.abs(np.diff(lists)))


print(f"Part 1, sum of distances = {total}")
