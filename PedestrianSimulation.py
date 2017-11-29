

class Pedestrian:

    def __init__(self, x, y):
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

T = 1000
t = 1000
dt = 0.1
N = 10
peds = []
pedRad = 0.2

#Centered at 0, walls will go from -20 to +20
wallXLength = 40
wallYLength = 40
target = (0, 20)


for i in range(N):
    peds.append(Pedestrian(-2*N*pedRad + 4*i*pedRad, -wallYLength/2 + 2*pedRad))

while t <= T:
    t += dt

    for p in peds:
        print(p.x)