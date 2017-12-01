import numpy as np
from scipy import integrate
import csv

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
        peds.append(Pedestrian(-2*N*radius + 4*i*radius, -wallYLength/2 + 2*radius, radius))
    return peds

def create_columns(n_cols):
    cols = []
    return cols


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
            #do stuff here
            return


def update_peds_vel(peds, dt):
    for p in peds:
        p.update_vel(dt)

def update_peds_pos(peds, dt):
    for p in peds:
        p.update_pos(dt)

def write_ped_data(writer, peds, t):
    for i, p in enumerate(peds):
        writer.writerow([t,i,p.x,p.y,p.vx,p.vy])

# calculate social force between pedestrians
# update array of pedestrians
def betweenPedestriansForce(peds):
    A = 0.2 # chosen arbitrarily because the paper doesn't suggest anything
    B = 5 # also chosen arbitrarily
    for p1 in peds: # for each pedestrian
        for p2 in peds: # calculate the social force from each other pedestrian
            if p1 == p2:
                continue
            r = p1.rad + p2.rad
            d = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            dy = np.abs(p1.y - p2.y)
            theta = np.arcsin(dy/d)
            f = A * np.exp((r-d)/B)
            fx = f * np.cos(theta)
            fy = f * np.sin(theta)
            p1.fx += fx
            p1.fy += fy


# Start main simulation
def run():
    T = 10
    t = 0
    dt = 0.1
    N = 10
    pedRad = 0.2
    peds = create_pedestrians(N, pedRad)
    outfile = "PedestrianData.csv"
    with open(outfile, 'w') as w:
        csv_writer = csv.writer(w, delimiter=',')
        csv_writer.writerow([N,wallXLength,wallYLength])
        while t <= T:
            for p in peds:
                p.fx = 0.0
                p.fy = 0.0

            betweenPedestriansForce(peds)

            update_peds_vel(peds, dt)
            wall_force(peds, dt)
            update_peds_vel(peds, dt)
            update_peds_pos(peds, dt)

            write_ped_data(csv_writer, peds, t)

            t += dt



run()










