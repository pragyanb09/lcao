import numpy as np

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from matplotlib.animation import FuncAnimation

x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
z = np.linspace(-5, 5, 20)

# print('x values:', x)

X, Y, Z = np.meshgrid(x, y, z)
# print(X.shape)
# print(X[0, 0, :5])

R = np.sqrt(X**2 + Y**2 + Z**2)  # distance from origin for each point
# print(R.shape)
# print(R[5, 5, 5])
# print(np.max(R))

a0 = 1.0
prob_density = np.exp(-2 * R / a0)
#print(prob_density[5, 5, 5])
#print(np.min(prob_density))
#print(np.max(prob_density))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

threshold = 0.001

mask = prob_density > threshold
xs = X[mask]
ys = Y[mask]
zs = Z[mask]
colors = prob_density[mask]

#print(len(xs))

scatter = ax.scatter(xs, ys, zs, c=colors, cmap="hot", alpha=0.6, s=20)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('1s Orbital')

def update(frame):
    ax.view_init(elev=20, azim=frame)
    return scatter,
    
ani = FuncAnimation(fig, update, frames=360, interval=50)

plt.show()

