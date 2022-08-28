import pygame
import sys
import pymunk
import math

STRING_LENGTH = 300*math.sqrt(2)

def convert_coordinates(point):
    return int(point[0]), int(1000-point[1])

def magnitude(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])

def angle(vector):
    return math.atan(vector[1]/vector[0])

def convert_vector(v):
    if v[0]==0:
        ang = math.pi/2 if v[1]>0 else -1*math.pi/2
    else:
        if v[0]<0:
            ang = angle(v)+math.pi
        else:
            ang = angle(v)+(2*math.pi) if v[1]<0 else angle(v)
    ang+=math.pi/2
    return (STRING_LENGTH*math.sin(ang), STRING_LENGTH*math.cos(ang))

class Ball():
    def __init__(self, x, y, m=1):
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, 50)
        self.shape.density = m
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    def draw(self):
        pygame.draw.circle(display, (255, 0, 0), convert_coordinates(self.body.position), 20)
    def move(self, x, y):
         self.body.position = (x, y)
        
class String():
    def __init__(self, body1, attachment, identifier="body"):
        self.body1 = body1
        if identifier == "body":
            self.body2 = attachment
        elif identifier == "position":
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = attachment
        joint = pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)
    def draw(self):
        pos1 = convert_coordinates(self.body1.position)
        pos2 = convert_coordinates(self.body2.position)
        pygame.draw.line(display, (0, 0, 0), pos1, pos2, 5)

pygame.init()
display = pygame.display.set_mode((1400, 1000))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 0)


def game():
    start = False
    points = []
    ball_1 = Ball(550, 750)
    ball_2 = Ball(400, 900, 10)
    # ball_1 = Ball(700, 500)
    # ball_2 = Ball(700, 400)
    string_1 = String(ball_1.body, (700, 600), "position")
    string_2 = String(ball_1.body, ball_2.body)
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.MOUSEBUTTONUP:
                start = True
                space.gravity = (0, -900)
            if pygame.mouse.get_pressed()[0] and start==False:
                space.gravity = (0, 0)
                pos = convert_coordinates(pygame.mouse.get_pos())
                v = convert_vector((pos[0]-700, pos[1]-600))
                ball_2.move(v[0]+700, -1*v[1]+600)
                ball_1.move((ball_2.body.position[0]+700)/2, (ball_2.body.position[1]+600)/2)
          
        display.fill((255, 255, 255))
        ball_1.draw()
        ball_2.draw()

        string_1.draw()
        string_2.draw()

        # if start == True:
        #     points.append(convert_coordinates(ball_2.body.position))
        #     for point in points:
        #         pygame.draw.circle(display, (0, 0, 255), point, 2)
        
        # if start==True:
        space.step(1/144)
        pygame.display.update()
        clock.tick(144)
game()
pygame.quit()
sys.exit()
