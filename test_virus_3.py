import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation

fig = plt.figure()
lim = 15
ax = plt.axes(xlim=(-lim, lim), ylim=(-lim, lim))

def gen():
    global track
    i = 0
    while track[1][-1] != 0:
        i += 1
        print(i)
        yield i

def animate(i):
    global points
    global velocities
    global states
    global n_points
    global track
    
    infection_rad = 0.5
    infection_rate = 0.75
    social_dist_rate = 0
    #social_dist_rate = track[0][-1]/n_points
    #social_dist_rate = 1-(track[0][-1]/n_points-1)**2
    
    for j in range(n_points):
        moved = False
        if social_dist_rate > 0:
            for k in range(n_points):
                vects = []
                if np.random.rand(1)[0] < social_dist_rate and k != j and (states[k] != 0.5 or states[j] != 0.5): #random rate every time
                    dist = (points[j][0]-points[k][0])**2 + (points[j][1]-points[k][1])**2
                    l = abs(np.random.normal(size=1, loc=0.2, scale=0.1)[0])
                    if states[k] == 1:
                        l *= 2
                    if dist < infection_rad:
                        vects.append([(points[j][0]-points[k][0])/dist*l,(points[j][1]-points[k][1])/dist*l])
        if social_dist_rate > 0 and vects != []:
            max_x = 0
            max_y = 0
            min_x = 0
            min_y = 0
            for k in range(len(vects)):
                if vects[k][0] > vects[max_x][0]:
                    max_x = k
                if vects[k][1] > vects[max_y][1]:
                    max_y = k
                if vects[k][0] < vects[min_x][0]:
                    min_x = k
                if vects[k][1] < vects[min_y][1]:
                    min_y = k
            velocities[j][0] = vects[max_x][0] + vects[min_x][0]
            velocities[j][1] = vects[max_y][1] + vects[min_y][1]
            points[j] += velocities[j]
        else:
            a,b = velocities[j]
            l = np.random.normal(size=1, loc=0.2, scale=0.1)[0]
            turn = np.random.normal(size=1, loc=0, scale=0.5)[0]
            theta = np.arctan2(b, a)+turn
            velocities[j][0] = l*np.cos(theta)
            velocities[j][1] = l*np.sin(theta)
            points[j] += velocities[j]
        
    track[0].append(track[0][-1])
    track[1].append(track[1][-1])
    track[2].append(track[2][-1])
    
    for j in range(n_points):
        point = points[j]
        vect = velocities[j]
        if inf_times[j] == 1:
            inf_times[j] = 0
            states[j] = 0.5
            track[2][-1] += 1
            track[1][-1] -= 1
        elif inf_times[j] > 1:
            inf_times[j] -= 1
        
        while point[0] > lim:
            point[0] -= np.random.rand(1)[0]
            vect[0] = -0.5
        while point[0] < -lim:
            point[0] += np.random.rand(1)[0]
            vect[0] = 0.5
        while point[1] > lim:
            point[1] -= np.random.rand(1)[0]
            vect[1] = -0.5
        while point[1] < -lim:
            point[1] += np.random.rand(1)[0]
            vect[1] = 0.5
    
    for j in range(n_points):
        for k in range(n_points):
            if k != j and states[j] == 1 and states[k] == 0:
                dist = (points[j][0]-points[k][0])**2 + (points[j][1]-points[k][1])**2
                if dist < infection_rad:
                    if np.random.rand(1)[0] < infection_rate*(infection_rad**2/dist+infection_rad):
                        states[k] = 1
                        track[1][-1] += 1
                        track[0][-1] -= 1
                        inf_times[k] = 150
    
    graph.set_offsets(points)
    graph.set_array(states)
    
    return graph,

n_points = 100
points = np.random.normal(size=(n_points,2), loc=0, scale=lim)
x = [points[0] for i in points]
y = [points[1] for i in points]

velocities = np.zeros((n_points,2))
states = np.zeros(n_points)
states[24] = 1
inf_times = np.zeros(n_points)
inf_times[24] = 150

graph = ax.scatter(x=x, y=y)

track = [[n_points-1],[1],[0]]

anim = FuncAnimation(fig, animate, frames=gen, interval=1, blit=True, repeat=False)

#anim.save('run_it.html')

plt.show()

plt.stackplot([i for i in range(0,len(track[0]))], track[1], track[0], track[2], colors=['m','c','r'])

plt.show()