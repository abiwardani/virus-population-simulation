import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N_points = 10

def update(num):
    new = np.random.normal(size=(N_points,2), loc=0, scale=1) 
    #debug_text.set_text("{:d}".format(num))  # for debugging
    #x,y,z = graph._offsets2d
    #new_x, new_y = (x+dx, y+dy)
    #graph.set_offsets([new_x, new_y])
    graph.set_offsets(new)
    #return [graph,debug_text]
    return graph

# create N_points initial points
x,y = np.random.normal(size=(2,N_points), loc=0, scale=10)

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot("111")
graph = ax.scatter(x, y, color='orange')
#debug_text = fig.text(0, 1, "TEXT", va='top')  # for debugging

# Creating the Animation object
ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
plt.show()