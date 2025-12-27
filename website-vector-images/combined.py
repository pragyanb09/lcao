import matplotlib.pyplot as plt
import numpy as np

#make grid
fig, ax = plt.subplots(figsize=(8, 8))

ax.set_xlim(-1, 5)
ax.set_ylim(-1, 5)

ax.set_aspect('equal')

ax.grid(True, alpha=0.5)

#add axes
ax.axhline(0, color='black', linewidth=1.5)
ax.axvline(0, color='black', linewidth=1.5)

ax.plot(0, 0, "ko", markersize=6)
ax.text(-0.3, -0.3, '0', fontsize=12)

xhat = np.array([1, 0])
yhat = np.array([0, 1])

ax.annotate('', 
    xy=(1,0),
    xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color='blue', linewidth=2.5))

ax.text(1.2, 0.1, r'$\hat{x}$', fontsize=14, color='blue')

ax.annotate('', 
    xy=(0, 1),
    xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color='red', linewidth=2.5))

ax.text(0.1, 1.2, r'$\hat{y}$', fontsize=14, color='red')

threex = np.array([3, 0])
twoy = np.array([0, 2])

ax.annotate('', 
    xy=(3, 0),
    xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color='green', linewidth=1.5))

ax.text(3.1,0.2, r'$3\hat{x}$', fontsize=14, color='green')

ax.annotate('', 
    xy=(0, 2),
    xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color='purple', linewidth=1.5))

ax.text(0.1, 2.1, r'$2\hat{y}$', fontsize=14, color='purple')

threetwo = np.array([3, 2])

ax.annotate('', 
    xy=(3, 2),
    xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color='orange', linewidth=1.5))

ax.text(3.1,2.1, r'$3\hat{x} + 2\hat{y}$', fontsize=14, color='orange')

plt.show()