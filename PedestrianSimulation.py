import numpy as np
import csv
import random


# pedestrian class to store all pedestrian data
class Pedestrian:
    # initialize a pedestrian with radius "size" at position (x, y)
    def __init__(self, x, y, size):
        self.rad = size
        self.m = 1.0
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.fx = 0.0
        self.fy = 0.0

    # update this pedestrian position from velocity
    def update_pos(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    # update this pedestrian velocity and remove force
    def update_vel(self, dt):
        self.vx += self.fx * dt
        self.vy += self.fy * dt
        self.fx = 0.0
        self.fy = 0.0


# makes N pedestrians randomly distributed in room
def create_pedestrians(N, radius):
    peds = []
    for i in range(N):
        px = (wallXLength - 1) * random.random() - wallXLength / 2
        py = (wallYLength / 3 + wallYLength / 2 - 1) * random.random() - wallYLength / 2
        peds.append(Pedestrian(px, py, radius))
    return peds


# create all columns
def create_columns():
    cols = [(-10, 0, 2.5), (10, 0, 2.5), (-10, 10, 2.5), (10, 10, 2.5)]
    return cols


# write all necessary pedestrian data to output file
def write_ped_data(writer, peds, t):
    for i, p in enumerate(peds):
        writer.writerow([t, i, p.x, p.y, p.vx, p.vy, p.rad])


# update velocity of all pedestrians from force
def update_peds_vel(peds, dt):
    for p in peds:
        p.update_vel(dt)


# update position of all pedestrians from velocity
def update_peds_pos(peds, dt):
    for p in peds:
        p.update_pos(dt)


# Change to set vel into wall = 0 if exists and force into wall = 0 if exists
def wall_force(peds, dt):
    wall_X = wallXLength / 2
    wall_Y = wallYLength / 2
    for p in peds:
        if np.abs(p.x) < 0.5 and p.y > wallYLength / 2 - p.rad or p.y > wallYLength / 2:
            continue
        if np.abs(p.x) > np.abs(wall_X - p.rad):
            if (p.x < 0 and (p.fx < 0 or p.vx < 0)) or (p.x > 0 and (p.fx > 0 or p.vx > 0)):
                p.fx = -p.vx / dt

        if np.abs(p.y) > np.abs(wall_Y - p.rad):
            if (p.y < 0 and (p.fy < 0 or p.vy < 0)) or (p.y > 0 and (p.fy > 0 or p.vy > 0)):
                p.fy = -p.vy / dt
    update_peds_vel(peds, dt)


# applies force from each column to each pedestrian necessary
def column_force(peds, cols, dt):
    for p in peds:
        for c in cols:
            colX = c[0]
            colY = c[1]
            colRad = c[2]
            d = colRad + p.rad

            dist = np.sqrt((colX - p.x) ** 2 + (colY - p.y) ** 2)
            if np.abs(p.x - colX) < colRad:
                if np.abs(colY - p.y) < (colRad + p.rad):
                    if ((colY - p.y) > 0 and p.vy > 0) or ((colY - p.y) < 0 and p.vy < 0):
                        p.fy = -p.vy / dt
            if np.abs(p.y - colY) < colRad:
                if np.abs(colX - p.x) < (colRad + p.rad):
                    if ((colX - p.x) > 0 and p.vx > 0) or ((colX - p.x) < 0 and p.vx < 0):
                        p.fx = -p.vx / dt
    update_peds_vel(peds, dt)


# calculate social force between pedestrians
# update array of pedestrians
def betweenPedestriansForce(peds, dt):
    A = 1  # chosen arbitrarily because the paper doesn't suggest anything
    B = 0.9  # also chosen arbitrarily
    for p1 in peds:  # for each pedestrian
        for p2 in peds:  # calculate the social force from each other pedestrian
            if p1 is p2:
                continue
            r = p1.rad + p2.rad
            d = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
            dy = np.abs(p1.y - p2.y)
            theta = np.arcsin(dy / d)
            temp = 1
            if (p1.x < p2.x):
                # theta += np.pite
                temp = -1
            temp1 = 1
            if (p1.y < p2.y):
                # theta += np.pite
                temp1 = -1
            if d < r:
                d = r
            f = A * np.exp((r - d) / B)
            fx = temp * f * np.cos(theta)
            fy = temp1 * f * np.sin(theta)
            p1.fx += fx
            p1.fy += fy
    update_peds_vel(peds, dt)


# calculate the walking force of each pedestrian
# Let's say the desired walking speed is 2
def walkingForce(peds, target, dt):
    ti = 0.5
    m = 1
    v0 = 3
    for p in peds:
        vtot = np.sqrt(p.vx ** 2 + p.vy ** 2)
        d = np.sqrt((p.x - target[0]) ** 2 + (p.y - target[1]) ** 2)
        dy = np.abs(p.y - target[1])
        theta = np.arcsin(dy / d)

        f = m * (v0 - vtot) / ti
        temp = 1
        if (p.x > target[0]):
            temp = -1
        fx = temp * f * np.cos(theta)
        fy = f * np.sin(theta)
        p.fx += fx
        p.fy += fy

    update_peds_vel(peds, dt)


# artificial speed limit for pedestrians in case they get launched accidentally
def limit_ped_speed(peds, max_vel):
    for p in peds:
        v = np.sqrt(p.vx ** 2 + p.vy ** 2)
        if np.sqrt(p.vx ** 2 + p.vy ** 2) > max_vel:
            p.vx *= max_vel / v
            p.vy *= max_vel / v
        if np.sqrt((p.x - target[0]) ** 2 + (p.y - target[1]) ** 2) < p.rad + .5:
            peds.remove(p)


# apply all the applicable forces to each pedestrian
def apply_ped_forces(peds, target, cols, dt):
    walkingForce(peds, target, dt)
    betweenPedestriansForce(peds, dt)
    wall_force(peds, dt)
    column_force(peds, cols, dt)


# start main simulation loop
def run():
    # define constants
    T = 60
    t = 0
    dt = 0.05
    N = 40
    pedRad = 1
    max_vel = 2

    # output data file location
    outfile = "../SimReaderTemp/PedestrianData.csv"

    # open data file for writing
    with open(outfile, 'w') as w:
        csv_writer = csv.writer(w, delimiter=',')
        # write header row
        csv_writer.writerow([N, wallXLength, wallYLength])

        # store created pedestrians
        peds = create_pedestrians(N, pedRad)
        # store created columns
        cols = create_columns()

        # add column info to data file
        for c in cols:
            csv_writer.writerow([-1, c[0], c[1], c[2]])

        # main loop
        while t <= T:
            print(t)
            # reset each pedestrian's force after each timestep
            for p in peds:
                p.fx = 0.0
                p.fy = 0.0

            # apply forces and move pedestrians
            apply_ped_forces(peds, target, cols, dt)
            update_peds_pos(peds, dt)
            limit_ped_speed(peds, max_vel)

            # write this timestep data
            write_ped_data(csv_writer, peds, t)

            # increment timestep
            t += dt


# Centered at 0, walls will go from -20 to +20
wallXLength = 40
wallYLength = 40

# location of pedestrian's target
target = (0, 30)

# start
run()
