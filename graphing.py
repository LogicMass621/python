#!/usr/bin/python

import pygame, sys
from pygame.locals import *

pygame.init()

black = [0, 0, 0]
white = [255, 255, 255]
green = [0,255,0]
blue = [0,0,255]
X=20
Y=380
X2 = 380
Y2 = 20

pygame.font.init()
display_surface = pygame.display.set_mode([X,Y])
font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('X', True, black, white)
textRect = text.get_rect()
textRect.center = (X // 2, Y // 2)

display_surface2 = pygame.display.set_mode([X2,Y2])
font = pygame.font.Font('freesansbold.ttf', 20)
text2 = font.render('Y', True, black, white)
textRect2 = text2.get_rect()
textRect2.center = (X2 // 2, Y2 // 2)

screen = pygame.display.set_mode([400,400])
pygame.display.set_caption('Graph')
screen.fill(white)

pygame.display.flip()
display_surface.blit(text, textRect)
display_surface2.blit(text2, textRect2)

class Graph:
    pygame.draw.line(screen,black, [200,0], [200,400],1)
    pygame.draw.line(screen,black,[0,200],[400,200],1)
    x = 200
    y=200

pygame.display.flip()
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
