#!/usr/bin/python

import pygame

black = [0, 0, 0]
white = [255, 255, 255]

screenWidth = 800
screenHeight = 800

graphWidth = 20
graphHeight = 20

sx= screenWidth / float(graphWidth)
sy= screenHeight / float(graphHeight)

Min = -graphWidth / 2
Max = graphWidth / 2
interval = 1 / sx

def tran(x,y):
    
    # scale
    x=x*sx
    y=y*sy

    # transform to screen coordinates
    x = screenWidth/2 + x
    y = screenHeight/2 - y
    
    return x,y

pygame.init()
pygame.font.init()
pygame.display.set_caption('Graph')

font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))

textX = font.render('X', True, black, white)
textY = font.render('Y', True, black, white)

textXWidth = textX.get_width() / sx

def compute_y(x):
    return x*x
    
def render():

    # x label
    screen.blit(textX, tran(graphHeight/2 - textXWidth,0))
    # y label
    screen.blit(textY, tran(0,graphWidth/2))

    # x-axis
    pygame.draw.line(screen,black, tran(-graphWidth/2,0), tran(graphWidth/2,0),1)
    # y-axis
    pygame.draw.line(screen,black, tran(0,graphHeight/2),tran(0,-graphHeight/2),1)

    x = Min
    y = compute_y(x)
    x2 = x
    y2 = y
        
    while x < Max:
        y = compute_y(x)
        pygame.draw.line(screen,black, tran(x2,y2) , tran(x,y) ,1)
        x2 = x
        y2 = y
        x = x + interval

running = True
while running:
    event = pygame.event.wait();
    if event.type == pygame.QUIT:
        running = False

    # clear screen to white
    screen.fill(white)
    render()
    pygame.display.update()
