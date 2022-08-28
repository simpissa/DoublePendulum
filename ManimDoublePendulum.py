import numpy as np
import math
from scipy.integrate import odeint
from manim import *

def RHS(y, t, m1, m2, l1, l2, g):
    theta1, theta2, w1, w2 = y
    w1dot = (l1*m2*math.cos(theta1 - theta2)*math.sin(theta1 - theta2)*w1**2 + l2*m2*math.sin(theta1 - theta2)*w2**2 - m2*g*math.cos(theta1 - theta2)*math.sin(theta2) + (m1 + m2)*g*math.sin(theta1)) / (l1*(math.cos(theta1 - theta2)**2*m2 - m1 - m2))
    w2dot = -(l2*m2*math.cos(theta1 - theta2)*math.sin(theta1 - theta2)*w2**2 + l1*(m1 + m2)*math.sin(theta1 - theta2)*w1**2 + (m1 + m2)*g*math.sin(theta1)*math.cos(theta1 - theta2) - (m1 + m2)*g*math.sin(theta2)) / (l2*(math.cos(theta1 - theta2)**2*m2 - m1 - m2))
    return w1, w2, w1dot, w2dot

def convert_coordinates(theta1, theta2, w1, w2, l1, l2):
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)
    return x1, y1, x2, y2

class DoublePendulum():
    def __init__(self, z, m1=1, m2=1, l1=1, l2=1, g=10):
        self.z0, self.m1, self.m2, self.l1, self.l2, self.g = z, m1, m2, l1, l2, g
        self.theta1, self.theta2, self.w1, self.w2 = z

        # self.x1, self.y1, self.x2, self.y2 = convert_coordinates(self.theta1, self.theta2, self.w1, self.w2, l1, l2)
    def getPosition(self):
        return self.x1, self.y1, self.x2, self.y2
    def getAngle(self):
        return self.theta1, self.theta2
    def getVelocity(self):
        return self.w1, self.w2
    def getMass(self):
        return self.m1, self.m2
    def step(self, dt, total):
        #if dt==0: return
        #t = np.arange(0, total, dt)
        t = [0, dt]

        z = odeint(RHS, self.z0, t, args=(self.m1, self.m2, self.l1, self.l2, self.g))

        #self.theta1, self.theta2, self.w1, self.w2 = self.z0[1]
        self.theta1, self.theta2, self.w1, self.w2 = z[1, 0], z[1, 1], z[1, 2], z[1, 3]
        self.z0 = self.theta1, self.theta2, self.w1, self.w2        

        # self.x1, self.y1, self.x2, self.y2 = convert_coordinates(self.theta1, self.theta2, self.w1, self.w2, l1, l2)

class AngleOverTime(Scene):
    def construct(self):
        size = 30
        
        pendulums = [[DoublePendulum([i*2*math.pi/(size-1) - math.pi, j*2*math.pi/(size-1) - math.pi, 0, 0]) for i in range(size)] for j in range(size)]

        def get_color(theta): 
            return [math.floor(128 + 127*math.sin(theta[0])*math.cos(theta[1])), math.floor(128 + 127*math.sin(theta[1])*math.sin(theta[0])), math.floor(128 + 127*math.cos(theta[0]))]
        
        def get_image():
            return np.uint8([[get_color(pendulums[i][j].getAngle()) for i in range(size)] for j in range(size)])

        def update_colors(img, dt):
             for i in range(size):
                 for j in range(size):
                     pendulums[i][j].step(dt, 2*dt)
             img.pixel_array = change_to_rgba_array(get_image())
            
                
        img = ImageMobject(get_image())
        img.height = 7

        self.add(img)

        img.add_updater(update_colors)
        self.wait(10)

class VelocityOverTime(Scene):
    def construct(self):
        size = 100
        G = 10
        max_v = math.sqrt(2*G)
        pendulums = [[DoublePendulum([0, 0, i*2*max_v/(size-1) - max_v, j*2*max_v/(size-1) - max_v]) for i in range(size)] for j in range(size)]

        def get_color(w, radius=127): 
            return [math.floor(127 + radius * math.cos(w[1]) * math.sin(w[0])), 
                        math.floor(127 + radius * math.sin(w[1]) * math.sin(w[0])),
                        math.floor(127 + radius * math.cos(w[0]))]
        
        def get_image():
            return np.uint8([[get_color(pendulums[i][j].getVelocity()) for i in range(size)] for j in range(size)])

        def update_colors(img, dt):
             
             for i in range(size):
                 for j in range(size):
                     pendulums[i][j].step(dt, 2*dt)
             img.pixel_array = change_to_rgba_array(get_image())
            
                
        img = ImageMobject(get_image())
        img.height = 7
        self.add(img)
        img.add_updater(update_colors)
        self.wait(10)

class RodLength(Scene):
    def construct(self):
        size = 100
        max_l = 10
        pendulums = [[DoublePendulum([math.pi/2, math.pi/2, 0, 0], l1=(i+1)*max_l/(size-1), l2=(j+1)*max_l/(size-1)) for i in range(size)] for j in range(size)]

        def get_color(l, radius=127): 
            return [math.floor(127 + radius * math.cos(l[1]) * math.sin(l[0])), 
                        math.floor(127 + radius * math.sin(l[1]) * math.sin(l[0])),
                        math.floor(127 + radius * math.cos(l[0]))]
        
        def get_image():
            return np.uint8([[get_color(pendulums[i][j].getAngle()) for i in range(size)] for j in range(size)])

        def update_colors(img, dt):
             
             for i in range(size):
                 for j in range(size):
                     pendulums[i][j].step(dt, 2*dt)
             img.pixel_array = change_to_rgba_array(get_image())
            
                
        img = ImageMobject(get_image())
        img.height = 7

        self.add(img)

        img.add_updater(update_colors)
        self.wait(10)
        
class Mass(Scene):
    def construct(self):
        size = 10
        max_m = 10
        pendulums = [[DoublePendulum([math.pi/2, math.pi/2, 0, 0], (i+1)*max_m/(size-1), (j+1)*max_m/(size-1)) for i in range(size)] for j in range(size)]

        def get_color(m, radius=127): 
            return [math.floor(127 + radius * math.cos(m[1]) * math.sin(m[0])), 
                        math.floor(127 + radius * math.sin(m[1]) * math.sin(m[0])),
                        math.floor(127 + radius * math.cos(m[0]))]
        
        def get_image():
            return np.uint8([[get_color(pendulums[i][j].getAngle()) for i in range(size)] for j in range(size)])

        def update_colors(img, dt):
             
             for i in range(size):
                 for j in range(size):
                     pendulums[i][j].step(dt, 2*dt)
             img.pixel_array = change_to_rgba_array(get_image())
            
                
        img = ImageMobject(get_image())
        img.height = 7

        self.add(img)

        img.add_updater(update_colors)
        self.wait(10)
