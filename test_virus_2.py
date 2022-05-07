import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')


fig = plt.figure()
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
line, = ax.plot([], [], lw=3)

def init():
    line.set_data([], [])
    return line,
def animate(i, n_points):
    global points
    points += np.random.normal(size=(2,n_points), loc=0, scale=0.5)
    line.set_data(points[0], points[1])
    return line,

n_points = 4
points = np.random.normal(size=(2,n_points), loc=0, scale=5)

print(np.random.normal(size=(2,n_points), loc=0, scale=0.5).shape)

anim = FuncAnimation(fig, animate, fargs=[n_points], frames=200, interval=100, blit=True)

plt.show()