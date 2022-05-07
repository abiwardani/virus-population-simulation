import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation

fig = plt.figure()
lim = 10
ax = plt.axes(xlim=(-lim, lim), ylim=(-lim, lim))

def gen():
    global track
    i = 0
    while track[1][-1] != 0:
        i += 1
        print(i)
        yield i

def init():
    global points
    graph.set_offsets(points)
    return graph,

def avoid_calc(j, infection_rad, social_dist_rate):
    global points
    global velocities
    global states
    global n_points
    
    if social_dist_rate > 0:
        vects = []
        for k in range(n_points):
            if np.random.rand(1)[0] < social_dist_rate and k != j and (states[k] != 0.5 or states[j] != 0.5) and (states[k]+states[j] == 1): #random rate every time
                dist = (points[j][0]-points[k][0])**2 + (points[j][1]-points[k][1])**2
                l = abs(np.random.normal(size=1, loc=0.2, scale=0.05)[0])
                if states[k] == 1:
                    l *= 2
                if dist < infection_rad:
                    vects.append([(points[j][0]-points[k][0])/dist*l,(points[j][1]-points[k][1])/dist*l])
    return vects
    
def avoid_exec(j, vects):
    global points
    global velocities
    global states
    global n_points
    
    max_x, max_y, min_x, min_y = (0, 0, 0, 0)
    maxx, maxy, minx, miny = (0, 0, 0, 0)
    for k in range(len(vects)):
        if vects[k][0] >= vects[max_x][0] and vects[k][0] > 0:
            maxx = 1
            max_x = k
        if vects[k][1] >= vects[max_y][1] and vects[k][1] > 0:
            maxy = 1
            max_y = k
        if vects[k][0] <= vects[min_x][0] and vects[k][0] < 0:
            minx = 1
            min_x = k
        if vects[k][1] <= vects[min_y][1] and vects[k][1] < 0:
            miny = 1
            min_y = k
    print(j, (vects[max_x][0] + vects[min_x][0]), (vects[max_y][1] + vects[min_y][1]))
    velocities[j][0] = vects[max_x][0]*maxx + vects[min_x][0]*minx
    velocities[j][1] = vects[max_y][1]*maxy + vects[min_y][1]*miny
    
    return None

def rand_move(j):
    global velocities
    
    a,b = velocities[j]
    l = abs(np.random.normal(size=1, loc=0.1, scale=0.05)[0])
    turn = np.random.normal(size=1, loc=0, scale=0.2)[0]
    theta = np.arctan2(b, a)+turn
    velocities[j][0] = l*np.cos(theta)
    velocities[j][1] = l*np.sin(theta)
    
    return None
    
def bounce_walls(lim):
    global points
    global velocities
    global states
    global inf_times
    global n_points
    global track
    
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
            point[0] -= np.random.rand(1)[0]/2
            vect[0] = -0.1
        while point[0] < -lim:
            point[0] += np.random.rand(1)[0]/2
            vect[0] = 0.1
        while point[1] > lim:
            point[1] -= np.random.rand(1)[0]/2
            vect[1] = -0.1
        while point[1] < -lim:
            point[1] += np.random.rand(1)[0]/2
            vect[1] = 0.1
            
    return None
    
def infect(j, infection_rad, infection_rate):
    global points
    global states
    global inf_times
    global n_points
    global track
    
    for k in range(n_points):
        if k != j and states[j] == 1 and states[k] == 0:
            dist = (points[j][0]-points[k][0])**2 + (points[j][1]-points[k][1])**2
            if dist < infection_rad:
                if np.random.rand(1)[0] < infection_rate*(infection_rad**2/dist+infection_rad):
                    states[k] = 1
                    track[1][-1] += 1
                    track[0][-1] -= 1
                    inf_times[k] = 150
                        
    return None

def new_record():
    global track
    
    track[0].append(track[0][-1])
    track[1].append(track[1][-1])
    track[2].append(track[2][-1])
    
    return None

def animate(i):
    global points
    global velocities
    global states
    global inf_times
    global n_points
    global track
    global lim
    
    infection_rad = 0.5
    infection_rate = 0.5
    social_dist_rate = 1
    #social_dist_rate = track[0][-1]/n_points
    #social_dist_rate = 1-(track[0][-1]/n_points-1)**2
    #social_dist_rate = 2*(1-(track[0][-1]/n_points-1)**2)**0.5
    
    for j in range(n_points):
        moved = False
        vects = avoid_calc(j, infection_rad, social_dist_rate)
        if social_dist_rate > 0 and vects != []:
            avoid_exec(j, vects)
            vects = []
        else:
            rand_move(j)
            vects = avoid_calc(j, infection_rad, social_dist_rate)
    
        points[j] += velocities[j]
        infect(j, infection_rad, infection_rate)
        
    new_record()
    bounce_walls(lim)
    
    graph.set_offsets(points)
    graph.set_array(states)
    
    return graph,

n_points = 100
initial_infections = 1

points = np.random.normal(size=(n_points,2), loc=0, scale=lim*0.75)
x = [points[0] for i in points]
y = [points[1] for i in points]

velocities = np.zeros((n_points,2))
states = np.zeros(n_points)
states[-initial_infections:] = [1 for i in range(initial_infections)]
inf_times = np.zeros(n_points)
inf_times[-initial_infections:] = [150 for i in range(initial_infections)]
inf_bar = np.zeros(n_points)

graph = ax.scatter(x=x, y=y)

track = [[n_points-initial_infections],[initial_infections],[0]]

anim = FuncAnimation(fig, animate, init_func=init, frames=gen, interval=50, blit=True, repeat=False, save_count=1000)

anim.save('run_it.html')

plt.show()

plt.stackplot([i for i in range(0,len(track[0]))], track[1], track[0], track[2], colors=['m','c','r'])

plt.show()