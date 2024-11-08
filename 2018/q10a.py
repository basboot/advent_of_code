import numpy as np

file1 = open('q10a.txt', 'r')

positions = []
velocities = []

for line in file1.readlines():
    # position=< 9,  1> velocity=< 0,  2>
    x, y, dx, dy = [int(x) for x in line.rstrip().replace("position=<", "").replace("> velocity=<", ",").replace(">", "").split(",")]

    positions.append((x, y))
    velocities.append((dx, dy))

positions = np.array(positions)
velocities = np.array(velocities)

t = 0
while True:
    new_positions = velocities + positions

    if np.max(positions, 0)[0] - np.min(positions, 0)[0] < np.max(new_positions, 0)[0] - np.min(new_positions, 0)[0]:
        break
    t += 1
    positions = new_positions

print(f"Waiting for {t} seconds")
import matplotlib.pyplot as plt

x = positions[:, 0]
y = -positions[:, 1]

# Step 4: Create the scatter plot
plt.scatter(x, y)

# Add labels and a title for clarity
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot of (x, y) coordinates')

# Show the plot
plt.show()