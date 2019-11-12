#!/usr/bin/python

import pygame

black = [0, 0, 0]
white = [255, 255, 255]

screenWidth = 400
screenHeight = 400

pygame.init()
pygame.font.init()
pygame.display.set_caption('Graph')

font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))

textX = font.render('X', True, black, white)
textRectX = textX.get_rect()
textY = font.render('Y', True, black, white)
textRectY = textY.get_rect()

def render():

    screenWidth = screen.get_width()
    screenHeight = screen.get_height()

    # clear screen to white
    screen.fill(white)

    textRectX.y = screenHeight/2 - textRectX.height
    textRectY.x = screenWidth/2 - textRectY.width

    screen.blit(textX, textRectX)
    screen.blit(textY, textRectY)

    pygame.draw.line(screen,black, [screenWidth/2,0], [screenWidth/2,screenHeight],1)
    pygame.draw.line(screen,black, [0,screenHeight/2],[screenWidth,screenHeight/2],1)

    pygame.display.update()

running = True
while running:
    event = pygame.event.wait();
    #print(event)
    if event.type == pygame.QUIT:
        running = False

    render()

