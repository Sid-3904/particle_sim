import random
from tkinter import *
from tkinter import Canvas
import numpy as np
from itertools import combinations
import time

HT = 600
WD = 800 
NUM = 10
G = 0.1
e = 0.99

root=Tk()
canvas=Canvas(root, height=HT, width=WD, bd=5, bg='grey')
canvas.pack()

class particle:
    def __init__(self, mass, charge, size = 10, color = 'black') :
        self.mass = mass
        self.charge = charge
        self.size = size
        self.color = color
        self.coord = [random.randint(2, WD-2), random.randint(2, HT-2)]
        self.velocity = [0, 0]
        self.p=canvas.create_oval(self.coord[0]-self.size, self.coord[1]-self.size, self.coord[0]+self.size, self.coord[1]+self.size, fill=self.color, outline='')

    def move(self) :
        if(self.coord[0]>WD or self.coord[0]<0) :
            self.velocity[0]=-self.velocity[0]
        if(self.coord[1]>HT or self.coord[1]<0) :
            self.velocity[1]=-self.velocity[1]
        self.coord[0] += self.velocity[0]
        self.coord[1] += self.velocity[1]
        canvas.coords(self.p, self.coord[0]-self.size, self.coord[1]-self.size, self.coord[0]+self.size, self.coord[1]+self.size)

def force(combo) :
    for i in combo :
        x = i[1].coord[0]-i[0].coord[0]
        y = i[1].coord[1]-i[0].coord[1]
        d = (x**2+y**2)**0.5
        s = y/d
        c = x/d
        if d>i[0].size+i[1].size :
            force = G*i[0].mass*i[1].mass/(d**2)
            i[0].velocity[0] += force*c/i[0].mass
            i[0].velocity[1] += force*s/i[0].mass
            i[1].velocity[0] -= force*c/i[1].mass
            i[1].velocity[1] -= force*s/i[1].mass
        else :
            ux1 = i[0].velocity[0]
            uy1 = i[0].velocity[1]
            ux2 = i[1].velocity[0]
            uy2 = i[1].velocity[1]
            i[0].velocity[0] = e*(ux2*(c**2) + uy2*s*c + ux1*(s**2) - uy1*s*c)
            i[0].velocity[1] = e*(ux2*s*c + uy2*(s**2) - ux1*s*c + uy1*(c**2))
            i[1].velocity[0] = e*(ux1*(c**2) + uy1*s*c + ux2*(s**2) - uy2*s*c)
            i[1].velocity[1] = e*(ux1*s*c + uy1*(s**2) - ux2*s*c + uy2*(c**2))


particles = []
for i in range(NUM) :
    particles.append(particle(1, 1))
combo = list(combinations(particles, 2))

#simulation loop
while True :
    for p in particles :
        p.move()
    force(combo)
    canvas.update()
