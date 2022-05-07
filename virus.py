import random as rd

class Board:
    def __init__(self,size,n):
        self.map = [[0 for i in range(size[1])] for j in range(size[0])]
        self.posns = [() for i in range(n)]
        self.states = ['H' for i in range(n)]
        
        for i in range(n):
            tpos = (rd.randint(0,size[0]),rd.randint(0,size[1]))
            while tpos in self.posns:
                tpos = (rd.randint(0,size[0]),rd.randint(0,size[1]))
            self.posns[i] = tpos
            self.map[size[0]][size[1]] = "O"
            
        self.rate = 0.25
        self.radius = 1
    
    def mprint(self):
        
        
    def infect(self,pos):
        x = pos[1]
        y = pos[0]
    
        for j in range(y-rad,y+rad+1):
            if j >=0 and j < self.size[0]:
                for i in range(x-rad,x+rad+1):
                    if i >= 0 and i < self.size[1]:
                        for k in range(n):
                            if self.posns[n] == (j,i) and rd.random() <= self.rate:
                                self.states[n] = "S"
    
    def move(self,pos):
        x = pos[1]
        y = pos[0]
        x_ = 0
        y_ = 0
        
        while 
            
            
        return (y+y_,x+x_)
        
    def run(self)
        
            
        