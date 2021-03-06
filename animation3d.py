#!/usr/bin/env python3
#
# n-body.py Solve the n-body problem using Newton
# 
# Copyright (C) 2019  Victor De la Luz (vdelaluz@enesmorelia.unam.mx)
#                      
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import numpy as np
plt.style.use('dark_background')


G=6.674e-11         #m^3kg^-1s^-2

class Particle:
    
    def __init__(self, p, v, m, dt=1):
        self.p = p #position
        self.v = v #velocity
        self.m = m #mass
        self.dt = dt
        self.trajectory = [p]
        self.time = [0.0]

    def setdt(self,dt):
        self.dt = dt

    def computeR(self,p1):
        r = math.sqrt( (p1[0]-self.p[0])**2 + (p1[1]-self.p[1])**2 + (p1[2]-self.p[2])**2)
        return r

    def computeU(self,p1):
        u=[0,0,0]
        i=0
        for a,b in zip(self.p,p1):
            u[i] = b - a
            i+=1
        return u
    
    #def integrate(self,dt,p1,m1):
    def integrate(self,B):
        r = self.computeR(B.p)
        u = self.computeU(B.p)

        Vx=(G*B.m*self.dt/(r**3))*u[0]
        Vy=(G*B.m*self.dt/(r**3))*u[1]
        Vz=(G*B.m*self.dt/(r**3))*u[2]

        
        self.v[0] += Vx
        self.v[1] += Vy
        self.v[2] += Vz
        
        self.p = [self.p[0]+ (self.v[0]) *dt,self.p[1]+ (self.v[1])*dt,self.p[2]+ (self.v[2])*dt]

    def getPosition(self):
        return self.p

    def getVelocity(self):
        return self.v

    def getKineticEnergy(self):
        k= (1/2)*self.m*(math.sqrt( self.v[0]^2 +self.v[1]^2+self.v[2]^2))
        return k    

    #def integrate(self,dt,p1,m1):
    def computeV(self,B):
        r = self.computeR(B.p)
        u = self.computeU(B.p)

        Vx=(G*B.m*self.dt/(r**3))*u[0]
        Vy=(G*B.m*self.dt/(r**3))*u[1]
        Vz=(G*B.m*self.dt/(r**3))*u[2]
        #print(u)
        #print(r)
        #print((G*B.m/(r**3))*u[0],(G*B.m/(r**3))*u[1],(G*B.m/(r**3))*u[2])         
        return [Vx,Vy,Vz]


    #def integrate(self,dt,p1,m1):
    def updateV(self,v):
        self.v[0] += v[0]
        self.v[1] += v[1]
        self.v[2] += v[2]
        
    #def integrate(self,dt,p1,m1):
    def updatePosition(self,time,save):        
        self.p = [self.p[0]+ (self.v[0]) *dt,self.p[1]+ (self.v[1])*dt,self.p[2]+ (self.v[2])*dt]
        if save:
            self.time.append(time)
            self.trajectory.append(self.p)


    def getTrajectory(self):
        return self.time, self.trajectory
        
class Potential:
    
    def __init__(self, system, dt):
        self.system = system #set of Particles
        self.dt = dt #set of Particles

    def integrate(self,time,save):
        #print(time/3600.0/24.0)
        for particle in self.system:
            for other in self.system:
                if other != particle:
                    velocity = particle.computeV(other)
                    particle.updateV(velocity)
        for particle in self.system:
            particle.updatePosition(time,save)

        return self.system

def gen(n, puntos):
    for p in puntos:
        yield np.array([p[0], p[1], p[2]])

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

    
# lenTime=3600.0*24*30*2  #sec (60 días)
lenTime=60*60*24 #  en segundos (periodo orbital de Mimas: 23 horas)
#lenTime=100
dt=1   #sec

# 1 segundo da los mejores resultados. Una menor dt provoca inestabilidad del sistema, quiza por problemas numericos, colapsando los cuerpos entre si

# Mas de 1 segundo tambien provoca problemas al verse disminuida la exactitud del modelo


# Saturno es el marco de referencia del sistema, por eso está en el origen y no tiene velocidades
saturn = Particle([0,0,0],[0,0,0],5.6834E+26)
'''
X =-7.336432675167782E-04*1.496e+11 
Y = 9.029757744771170E-04*1.496e+11 
Z =-4.400017633666113E-04*1.496e+11
VX=-6.722716075791823E-03*1.496e+11 
VY=-3.906534056535731E-03*1.496e+11 
VZ= 2.741552242697911E-03*1.496e+11
'''

import json
lunas = ["Mimas", "Encelados", "Tethys", "Dione", "Rhea", "Titan", "Iapetus"]
# lunas = ["Mimas", "Encelados", "Tethys", "Dione"]
# lunas = ["Mimas", "Encelados"]
with open('lunas.json') as json_file:
    luna = json.load(json_file)

# Todas las cantidades deben estar en unidades de metros y segundos
for l in lunas:
    for i in range(3):
        luna[l][0][i] *= 1000
        luna[l][1][i] *= 1000
'''        
X =-1.097514706739005E+08
Y = 1.350832531554601E+08
Z =-6.582332690389031E+07
VX=-1.164009271133237E+04
VY=-6.763995100402531E+03
VZ= 4.746879374078901E+03
mimas = Particle([X,Y,Z],[VX,VY,VZ],3.75E+19)
'''
particles = [saturn]
for l in lunas:
    particles.append(Particle(*luna[l], dt=dt)) # Pasa cada elemento de la lista como un parametro

#mimas = Particle(*luna['Mimas'])
#mimas = Particle([X,Y,Z],[0,0,0],3.75E+19)
n_steps = int(lenTime/dt)

nBody = Potential(particles,dt)

x=[]
y=[]


skip=0        # Mas eficiente
save=False
#n_steps = 3

print(str(1)+'/'+str(n_steps))
for time in range(1,n_steps):
	print(str(time+1)+'/'+str(n_steps))
	if skip == 5000:
	    skip=0
	    save=True
	system = nBody.integrate(float(time)*dt,save)
	save=False
	skip += 1
	#if t==1000000:
	#	break



fig = plt.figure()
ax = p3.Axes3D(fig)
#! ax = fig.add_subplot(111, projection='3d')

puntos = []
dim = []

i=0
c=['g','r','b','g','r','b','g','r','b','g','r','b']
for particle in particles:
    pts = []
    t, trajectory = particle.getTrajectory()
    if round(sum(particle.v)) == 0:
        for x, y in zip(t,trajectory):
            ax.scatter(y[0], y[1], y[2], s=20, marker='o', c='palegoldenrod')
            #ax.scatter(y[0], y[1], y[2], c=c[i])
    else:
        for x, y in zip(t,trajectory):
            # ax.scatter(y[0], y[1], y[2], s=5, marker='o',c=c[i])
            # a = ax.scatter(y[0], y[1], y[2], s=5, marker='o',c=c[i])
            a = ax.plot(y[0], y[1], y[2])[0]
            b = (y[0], y[1], y[2])

            pts.append(b)
            dim.append(b)
            # three_dim.append(c)
            #ax.scatter(y[0], y[1], y[2], c=c[i])
    if len(pts) == 0:
        continue
    else:
        puntos.append(pts)
    i=i+1

# for p in puntos:
#     print(p)

#! Cambiar l para plotear Luna
'''
0 Mimas
1 Encelados
2 Tethys 
3 Dione 
4 Rhea 
5 Titan 
6 Iapetus
'''
l = 1
data = np.array(list(gen(len(puntos), puntos[l]))).T
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

ani = animation.FuncAnimation(fig, update, len(puntos[l]), fargs=(data, line), interval=10000/len(puntos[l]), blit=False)

plt.show()
