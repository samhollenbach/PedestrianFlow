import numpy
from scipy import integrate

class Pedestrian:

    def __init__(self, x, y):
        self.m = 1.0
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.fx = 0.0
        self.fy = 0.0

    def update(self, dt):
        self.vx += self.fx*dt
        self.vy += self.fy*dt
        self.x += self.vx*dt
        self.y += self.vy*dt


#Centered at 0, walls will go from -20 to +20
wallXLength = 40
wallYLength = 40
target = (0, 20)

# Makes N pedestrians evenly distributed
def create_pedestrians(N,radius):
    peds = []
    for i in range(N):
        peds.append(Pedestrian(-2*N*radius + 4*i*radius, -wallYLength/2 + 2*radius))
    return peds

# Start main simulation
def run():
    T = 1000
    t = 1000
    dt = 0.1
    N = 10
    pedRad = 0.2
    peds = create_pedestrians(N, pedRad)

    while t <= T:
        t += dt
        for p in peds:
            print(p.x)

run()

# calculate social force between pedestrians
# this will return a list of the x and y components of social
# force for each pedestrian
def betweenPedestriansForce(peds):
    for p in peds:
        print(p.x)



