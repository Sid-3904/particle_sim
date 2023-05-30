import random
from tkinter import *
from tkinter import Canvas
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import time
from scipy.stats import norm

HT = 600
WD = 800 
NUM = 200
SIZE = 2
COLOR = 'black'

root=Tk()
canvas=Canvas(root, height=HT, width=WD, bd=5, bg='white')
canvas.pack()

class particle:
    def __init__(self) :
        self.coord = [random.randint(2, WD-2), random.randint(2, HT-2)]
        self.velocity = [random.choice([1, -1])*random.random(), random.choice([1, -1])*random.random()]
        self.p=canvas.create_oval(self.coord[0]-SIZE, self.coord[1]-SIZE, self.coord[0]+SIZE, self.coord[1]+SIZE, fill=COLOR, outline='')

    def move(self) :
        if(self.coord[0]>WD or self.coord[0]<0) :
            self.velocity[0]=-self.velocity[0]
        if(self.coord[1]>HT or self.coord[1]<0) :
            self.velocity[1]=-self.velocity[1]
        self.coord[0] += self.velocity[0]
        self.coord[1] += self.velocity[1]
        canvas.coords(self.p, self.coord[0]-SIZE, self.coord[1]-SIZE, self.coord[0]+SIZE, self.coord[1]+SIZE)

def collide(combos) :
    for i in combos :
        x = i[1].coord[0]-i[0].coord[0]
        y = i[1].coord[1]-i[0].coord[1]
        d = (x**2+y**2)**0.5
        if d <= 4*SIZE :
            s = y/d
            c = x/d
            ux1 = i[0].velocity[0]
            uy1 = i[0].velocity[1]
            ux2 = i[1].velocity[0]
            uy2 = i[1].velocity[1]
            i[0].velocity[0] = ux2*(c**2) + uy2*s*c + ux1*(s**2) - uy1*s*c
            i[0].velocity[1] = ux2*s*c + uy2*(s**2) - ux1*s*c + uy1*(c**2)
            i[1].velocity[0] = ux1*(c**2) + uy1*s*c + ux2*(s**2) - uy2*s*c
            i[1].velocity[1] = ux1*s*c + uy1*(s**2) - ux2*s*c + uy2*(c**2)

particles = []
for i in range(NUM) :
    particles.append(particle())
combos = list(combinations(particles, 2))

#simulation loop
for t in range(2000):
    for p in particles :
        p.move()
    collide(combos)
    canvas.update()

v_data = []
E_data = []
for p in particles :
    v = (p.velocity[0]**2 + p.velocity[1]**2)**0.5
    E = p.velocity[0]**2 + p.velocity[1]**2
    v_data.append(v)
    E_data.append(E)
    

v_weights = 10*np.ones_like(v_data)/len(v_data)
E_weights = 10*np.ones_like(E_data)/len(E_data)
plt.hist(E_data, weights=E_weights, bins = 25, color = 'green')
plt.hist(v_data, weights=v_weights, bins = 25)
v_mu, v_std = norm.fit(v_data)
E_mu, E_std = norm.fit(E_data)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
v_p = norm.pdf(x, v_mu, v_std)
E_p = norm.pdf(x, E_mu, E_std)
plt.plot(x, v_p, 'k', linewidth=2)
plt.plot(x, E_p, 'k', linewidth=2, color = 'red')
plt.title("v & E distribution") 
plt.show()