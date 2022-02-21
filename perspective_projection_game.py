import random
import math
import numpy as np
import pygame
from pygame.locals import *
# need to find a different way of computing the spanning vectors
# division by zero when z component of normal is zero
class Camera:
    def __init__(self, origin, normal):
        self.origin = origin
        self.normal = normal
    def spanningVectors(self):
        norm = self.normal
        v1 = [1, 0, 0]
        v1[2] = -(v1[0]*norm[0] + v1[1]*norm[1])
        v2 = [0, 1, 0]
        v2[2] = -(v2[0]*norm[0] + v2[1]*norm[1])
        v1 = np.array(v1)
        length = np.linalg.norm(v1)
        v1 = v1 / length if length != 0 else v1
        v2 = np.array(v2)
        length = np.linalg.norm(v2)
        v2 = v2 / length if length != 0 else v2
        return v1.tolist(), v2.tolist()
    def project(self, points):
        orig = self.origin
        norm = self.normal
        projection = dict()
        f = np.array(orig) + np.array(norm)
        v1, v2 = self.spanningVectors()
        for p in points:
            projection[p] = None
            A = np.array(
                [[v1[0], v2[0], p[0]-f[0]],
                 [v1[1], v2[1], p[1]-f[1]],
                 [v1[2], v2[0], p[2]-f[2]]])
            b = -f
            x = np.linalg.solve(A, b)
            # retina is not between rendered point and focal point
            if np.linalg.norm(np.array(p)-x) > np.linalg.norm(np.array(p)-f):
                continue
            projection[p] = (v1[0]*x[1] + v2[0]*x[2], v1[1]*x[1] + v2[1]*x[2])
        return projection
    def dist(self, v1, v2):
        return sum([x**2-v2[i]**2 for i,x in enumerate(v1)])**0.5
    # Move the camera origin to v, maintaining it's heading
    def reposition(self, v):
        delta = tuple(x-self.origin[i] for i,x in enumerate(v))
        for i,x in enumerate(delta):
            self.normal[i] += x
            self.origin[i] = v[i]

    # Point the camera to v, maintaining position
    def orient(self, v):
        dist1 = sum([x**2-self.origin[i]**2 for i,x in enumerate(self.normal)])**0.5
        dist2 = sum([x**2-self.origin[i]**2 for i,x in enumerate(v)])**0.5
        for i,x in enumerate(self.normal):
            self.normal[i] = -1*v/dist2*dist1


camera = Camera([0,0,-5], [0,0,-1])

points = {tuple(random.random() for i in range(3)) for j in range(3)}

pygame.init()

size = [400, 300]
screen = pygame.display.set_mode([x*2 for x in size])
pygame.display.set_caption("Example code")

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    temp = [0,0]
    temp[0] = camera.normal[0]*math.cos(0.01)-camera.normal[1]*math.sin(0.01)
    temp[1] = camera.normal[0]*math.sin(0.01)+camera.normal[1]*math.cos(0.01)
    camera.normal[0] = temp[0]
    camera.normal[1] = temp[1]  
    screen.fill((255,255,255))
    projection = camera.project(points)
    for key in projection:
        if projection[key] is None:
            continue
        pos = [round(projection[key][i]*size[i]/2+size[i]/2) for i in range(2)]
        pygame.draw.circle(screen, (0,0,0), pos, 1)
    pygame.display.update()

pygame.quit()

