import numpy as np
from scipy import integrate
import csv
import random
import decimal

class Pedestrian:

    def __init__(self, x, y, size):
        self.rad = size
        self.m = 1.0
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.fx = 0.0
        self.fy = 0.0

    def update_pos(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def update_vel(self, dt):
        self.vx += self.fx*dt
        self.vy += self.fy*dt
        self.fx = 0.0
        self.fy = 0.0
        


#Centered at 0, walls will go from -20 to +20
wallXLength = 40
wallYLength = 40
target = (0, 20)

# Makes N pedestrians evenly distributed
def create_pedestrians(N,radius):
    peds = []
    for i in range(N):
        px = wallXLength/2 * float(random.randrange(-99, 99))/100
        py = wallYLength/2 * float(random.randrange(-99, 99))/100
        peds.append(Pedestrian(px, py, radius))
    return peds

def create_columns(n_cols):
    cols = [(0, 0, 3)]
    return cols


def update_peds_vel(peds, dt):
    for p in peds:
        p.update_vel(dt)

def update_peds_pos(peds, dt):
    for p in peds:
        p.update_pos(dt)

# Change to set vel into wall = 0 if exists and force into wall = 0 if exists
def wall_force(peds, dt):
    wall_X = wallXLength/2
    wall_Y = wallYLength/2
    for p in peds:
        if np.abs(p.x) > np.abs(wall_X-p.rad):
            p.fx = -p.vx/dt
        if np.abs(p.y) > np.abs(wall_Y-p.rad):
            p.fy = -p.vy/dt


def column_force(peds, cols, dt):
    for p in peds:
        for c in cols:
            colX = c[0]
            colY = c[1]
            colRad = c[2]
            d = colRad + p.rad

            dist = np.sqrt((colX-p.x)**2 + (colY-p.y)**2)
            if dist <= d:
                theta = np.arcsin((colY-p.y)/dist)
                if (p.y > colY):
                    theta += np.pi
                p.fx += -np.cos(theta)*p.vx/dt
                p.fy += -np.sin(theta)*p.vy/dt



def write_ped_data(writer, peds, t):
    for i, p in enumerate(peds):
        writer.writerow([t,i,p.x,p.y,p.vx,p.vy,p.rad])

# calculate social force between pedestrians
# update array of pedestrians
def betweenPedestriansForce(peds):
    A = 0.2 # chosen arbitrarily because the paper doesn't suggest anything
    B = 1 # also chosen arbitrarily
    for p1 in peds: # for each pedestrian
        for p2 in peds: # calculate the social force from each other pedestrian
            if p1 is p2:
                continue
            r = p1.rad + p2.rad
            d = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            dy = np.abs(p1.y - p2.y)
            theta = np.arcsin(dy/d)
            temp = 1
            if (p1.x < p2.x):
                #theta += np.pite
                temp = -1
            temp1 = 1
            if (p1.y < p2.y):
                #theta += np.pite
                temp1 = -1
            f = A * np.exp((r-d)/B)
            fx = temp*f * np.cos(theta)
            fy = temp1*f * np.sin(theta)
            p1.fx += fx
            p1.fy += fy

# calculate the walking force of each pedestrian
# Let's say the desired walking speed is 2
def walkingForce(peds, target):
    ti = 0.5
    m = 1
    v0 = 1
    for p in peds:
        vtot = np.sqrt(p.vx**2 + p.vy**2)
        d = np.sqrt((p.x - target[0]) ** 2 + (p.y - target[1]) ** 2)
        dy = np.abs(p.y - target[1])
        theta = np.arcsin(dy / d)

        f = m*(v0 - vtot)/ti
        temp = 1
        if (p.x > target[0]):
            temp = -1
        fx = temp*f * np.cos(theta)
        temp1 = 1
        if (p.xy > target[0]):
            temp1 = -1
        fy = temp1*f * np.sin(theta)
        p.fx += fx
        p.fy += fy



# Start main simulation
def run():
    T = 150
    t = 0
    dt = 0.1
    N = 25
    pedRad = 1
    peds = create_pedestrians(N, pedRad)
    outfile = "../SimReaderTemp/PedestrianData.csv"


    with open(outfile, 'w') as w:
        csv_writer = csv.writer(w, delimiter=',')
        csv_writer.writerow([N,wallXLength,wallYLength])
        cols = []
        for c in cols:
            csv_writer.writerow([-1,c[0],c[1],c[2]])
        while t <= T:
            for p in peds:
                p.fx = 0.0
                p.fy = 0.0

            walkingForce(peds, target)
            update_peds_vel(peds,dt)
            betweenPedestriansForce(peds)

            update_peds_vel(peds, dt)
            wall_force(peds, dt)
            update_peds_vel(peds,dt)
            column_force(peds,cols,dt)
            update_peds_vel(peds, dt)
            update_peds_pos(peds, dt)

            for p in peds:
                if np.sqrt((p.x-target[0])**2 + (p.y-target[1])**2) < p.rad+.5:
                    peds.remove(p)

            write_ped_data(csv_writer, peds, t)

            t += dt



run()










