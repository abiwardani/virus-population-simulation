import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation

#--- Simulation infrastructure

class Simulation:
    def __init__(self, lim, n, init_infect=1, infect_rad=0.5, infect_rate=0.5, cure_time=150, trigger=0, social_dist=0):
        self.lim = lim #set frame size limit
        self.n_points = n #set number of people
        self.initial_infections = init_infect #set number of initially infected people
        self.cure_time = cure_time #set duration of individual infection
        
        self.fig = plt.figure() #make figure
        
        self.ax = plt.axes(xlim=(-lim, lim), ylim=(-lim, lim)) #draw axes
        
        self.points = np.random.normal(size=(self.n_points,2), loc=0, scale=self.lim*0.75) #place people onto map
        self.velocities = np.zeros((self.n_points,2)) #set initial movement
        self.states = np.zeros(self.n_points)
        self.states[-self.initial_infections:] = [1 for i in range(self.initial_infections)] #set everyone as healthy, except for initial_infections people; 0 = healthy, 1 = infected, 0.5 = eliminated (unintuitive numbering to ease coloring)
        self.inf_times = np.zeros(self.n_points)
        self.inf_times[-self.initial_infections:] = [self.cure_time for i in range(self.initial_infections)] #set all infection time as 0, except for initially infected people
        self.track = [[self.n_points-self.initial_infections],[self.initial_infections],[0]] #make case count for each frame: track[0] = healthy, track[1] = infected, track[2] = eliminated
        
        self.infection_rad = infect_rad #set infection radius
        self.infection_rate = infect_rate #set infection rate
        self.trigger = trigger #set trigger date
        
        if social_dist == "proportional":
            self.social_dist_rate = 2*self.track[1][-1]/self.n_points #social distancing rate proportional to percent population infected
        elif social_dist == "cubic1":
            self.social_dist_rate = 1-(1.35*self.track[1][-1]/self.n_points-1)**3 #social distancing rate proportional to percent population infected cubed
        elif social_dist == "cubic2":
            self.social_dist_rate = (1-(1.5*self.track[1][-1]/self.n_points-1)**3)**0.5 #social distancing rate following rounded cubic arc
        elif self.trigger > 0:
            self.social_dist_rate = 0
            self.social_dist_trigger = social_dist
        else:
            self.social_dist_rate = float(social_dist)
        
        x = [self.points[0] for i in self.points]
        y = [self.points[1] for i in self.points]
        
        self.graph = self.ax.scatter(x=x, y=y)
        
        return None
    
    def gen(self):
        i = 0
        while self.track[1][-1] != 0:
            i += 1
            print(i)
            yield i
    
    def init(self):
        self.graph.set_offsets(self.points)
        return self.graph,
        
    def avoid_calc(self, j):
        if self.social_dist_rate > 0:
            vects = []
            for k in range(self.n_points):
                if np.random.rand(1)[0] < self.social_dist_rate and k != j and (self.states[k] != 0.5 or self.states[j] != 0.5) and (self.states[k]+self.states[j] == 1): #random rate every time
                    dist = (self.points[j][0]-self.points[k][0])**2 + (self.points[j][1]-self.points[k][1])**2
                    l = abs(np.random.normal(size=1, loc=0.2, scale=0.05)[0])
                    if self.states[k] == 1:
                        l *= 2
                    if dist < self.infection_rad:
                        vects.append([(self.points[j][0]-self.points[k][0])/dist*l,(self.points[j][1]-self.points[k][1])/dist*l])
        return vects
    
    def avoid_exec(self, j, vects):
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
        self.velocities[j][0] = vects[max_x][0]*maxx + vects[min_x][0]*minx
        self.velocities[j][1] = vects[max_y][1]*maxy + vects[min_y][1]*miny
        
        return None
    
    def rand_move(self, j):
        a,b = self.velocities[j]
        l = abs(np.random.normal(size=1, loc=0.1, scale=0.05)[0])
        turn = np.random.normal(size=1, loc=0, scale=0.2)[0]
        theta = np.arctan2(b, a)+turn
        self.velocities[j][0] = l*np.cos(theta)
        self.velocities[j][1] = l*np.sin(theta)
        
        return None
    
    def bounce_walls(self):
        for j in range(self.n_points):
            point = self.points[j]
            vect = self.velocities[j]
            if self.inf_times[j] == 1:
                self.inf_times[j] = 0
                self.states[j] = 0.5
                self.track[2][-1] += 1
                self.track[1][-1] -= 1
            elif self.inf_times[j] > 1:
                self.inf_times[j] -= 1
            
            while point[0] > self.lim:
                point[0] -= np.random.rand(1)[0]/2
                vect[0] = -0.1
            while point[0] < -self.lim:
                point[0] += np.random.rand(1)[0]/2
                vect[0] = 0.1
            while point[1] > self.lim:
                point[1] -= np.random.rand(1)[0]/2
                vect[1] = -0.1
            while point[1] < -self.lim:
                point[1] += np.random.rand(1)[0]/2
                vect[1] = 0.1
                
        return None
    
    def infect(self, j):
        for k in range(self.n_points):
            if k != j and self.states[k] == 0:
                dist = (self.points[j][0]-self.points[k][0])**2 + (self.points[j][1]-self.points[k][1])**2
                if dist < self.infection_rad:
                    if np.random.rand(1)[0] < self.infection_rate*(self.infection_rad**2/dist+self.infection_rad):
                        self.states[k] = 1
                        self.track[1][-1] += 1
                        self.track[0][-1] -= 1
                        self.inf_times[k] = self.cure_time
                        
        return None
    
    def new_record(self):
        self.track[0].append(self.track[0][-1])
        self.track[1].append(self.track[1][-1])
        self.track[2].append(self.track[2][-1])
    
        return None

    def animate(self, i):
        if self.trigger != 0 and i == self.trigger:
            self.social_distance_rate = self.social_distance_trigger
    
        for j in range(self.n_points):
            moved = False
            vects = self.avoid_calc(j)
            if self.social_dist_rate > 0 and vects != []:
                self.avoid_exec(j, vects)
                vects = []
            else:
                self.rand_move(j)
    
            self.points[j] += self.velocities[j]
            
            if self.states[j] == 1:
                self.infect(j)
        
        self.new_record()
        self.bounce_walls()
    
        self.graph.set_offsets(self.points)
        self.graph.set_array(self.states)
    
        return self.graph,
    
    def run(self, show, filename=None):
        anim = FuncAnimation(self.fig, self.animate, init_func=self.init, frames=self.gen, interval=50, blit=True, repeat=False, save_count=1000)
        if filename != None:
            ext = 1+filename.index(".")
            if filename[ext:] != "html":
                filename = filename[:ext]
                filename += "html"
        
            anim.save(filename)
        
        if show:
            plt.show()
    
    def stats(self, show, filename=None):
        plt.stackplot([i for i in range(0,len(self.track[0]))], self.track[1], self.track[0], self.track[2], colors=['m','c','r'])
        if filename != None:
            plt.savefig(filename)
        
        if show:
            plt.show()

#--- Simulating the virus

my_sim = Simulation(10, 20, init_infect=3, infect_rad=0.5, infect_rate=1, cure_time=1000, social_dist=1)

my_sim.run(False, "run_it.html")

my_sim.stats(False, "ran_it.png")


    
    