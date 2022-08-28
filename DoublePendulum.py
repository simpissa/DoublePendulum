from graphics import *
import numpy as np
import math
import time

WIDTH = 1000
HEIGHT = 1000

M1 = 1
M2 = 1
G = 10
L1 = 1
L2 = 1
THETA_1 = math.pi/4
THETA_2 = math.pi/4
H = 0.001

def convert_coordinates(x, y):
    return x+(WIDTH/2), (HEIGHT/2)-y

def scale_coordinate(x):
    v = x*500/math.pi if x<= math.pi else (x-2*math.pi)*500/math.pi
    return v*2
    # return x*1000/(2*math.pi)

window = GraphWin("Double Pendulum", WIDTH, HEIGHT)
ball1 = Circle(Point(convert_coordinates(0, -100)[0], convert_coordinates(0, -100)[1]), 20)
ball2 = Circle(Point(convert_coordinates(0, -200)[0], convert_coordinates(0, -200)[1]), 20)
ball1.setFill("red")
ball2.setFill("red")
rod1 = Line(Point(WIDTH/2, HEIGHT/2), ball1.getCenter())
rod2 = Line(ball1.getCenter(), ball2.getCenter())

def RHS(y):
    theta1, theta2, omega1, omega2 = y
    return np.array([ theta1, theta2, 
                      (M2*L1*omega1**2*math.sin(theta1-theta2) + 2*M2*L2*omega2**2*math.sin(theta1-theta2) + 2*G*M2*math.cos(theta2)*math.sin(theta1-theta2) + 2*G*M1*math.sin(theta1)) / (-2*L1*(M1 + M2*math.sin(theta1-theta2)**2)), 
                      (M2*L2*omega2**2*math.sin(theta1-theta2) + 2*(M1 + M2)*L1*omega1**2*math.sin(theta1-theta2) + 2*G*(M1 + M2)*math.cos(theta1)*math.sin(theta1-theta2)) / (2*L2*(M1 + M2*math.sin(theta1-theta2)**2)) ])

def step(theta1, theta2, t):
    #Runge-Kutta
    omega1 = ball1.getAngularVelocity()
    omega2 = ball2.getAngularVelocity()
    #update theta
    theta1 += omega1*H
    theta2 += omega2*H
    theta1 %= 2*math.pi
    theta2 %= 2*math.pi
    
    y = [theta1, theta2, omega1, omega2]
    
    #update omega
    k1 = RHS(y)
    k2 = RHS(y + k1*H/2)
    k3 = RHS(y + k2*H/2)
    k4 = RHS(y + k3*H)
    dy = (k1 + 2*k2 + 2*k3 + k4) * H/6
    
    ball1.setAngularVelocity(omega1+dy[2])
    ball2.setAngularVelocity(omega2+dy[3])
    
    return theta1, theta2, t+H

def draw(theta1, theta2):
    x1 = 200 * math.sin(theta1)
    y1 = -200 * math.cos(theta1)
    x2 = 200 * math.sin(theta2) + x1
    y2 = y1 - 200 * math.cos(theta2)
    
    ball1.goTo(convert_coordinates(x1, y1)[0], convert_coordinates(x1, y1)[1])
    ball2.goTo(convert_coordinates(x2, y2)[0], convert_coordinates(x2, y2)[1])
    rod1.goTo(Point(WIDTH/2, HEIGHT/2), ball1.getCenter())
    rod2.goTo(ball1.getCenter(), ball2.getCenter())
    
    # rod1.undraw()
    # rod1.draw(window)
    # rod2.undraw()
    # rod2.draw(window)

    #time.sleep(H)

def main():
    t = 0
    # ball1.draw(window)
    # ball2.draw(window)
    # rod1.draw(window)
    # rod2.draw(window)
    
    xaxis = Line(Point(0, 500), Point(1000, 500))
    yaxis = Line(Point(500, 0), Point(500, 1000))
    xaxis.draw(window)
    yaxis.draw(window)
    
    theta1 = THETA_1
    theta2 = THETA_2
    while t < 1000:
        theta1, theta2, t = step(theta1, theta2, t)
        
        point = Circle(Point(scale_coordinate(theta1)+500, 500-scale_coordinate(theta2)), 1)
        point.setFill("blue")
        point.draw(window)
        
        draw(theta1, theta2)
    
    print("finish")
    window.getMouse()
    
main()
