#!/usr/bin/python
import pygame, sys
from pygame.locals import *

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (158,  52,   45)
GREEN = (  125, 130,   0)
BLUE  = (  0,   255, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, BLUE, ((146, 0), (600, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, GREEN, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
pygame.draw.circle(DISPLAYSURF, GREEN, (300, 50), 20, 0)
pygame.draw.ellipse(DISPLAYSURF, RED, (420, 320, 40, 80), 0)
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[380][542] = BLUE
pixObj[382][544] = BLACK
pixObj[384][546] = BLUE
pixObj[386][548] = BLACK
pixObj[388][550] = BLUE
del pixObj

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
