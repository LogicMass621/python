#!/usr/bin/python

import pygame

black = [0, 0, 0]
white = [255, 255, 255]

screenWidth = 800
screenHeight = 800

Min = -screenWidth/2#float(input('What is the lower number in the domain:'))
Max = screenWidth/2#float(input('What is the higher number in the domain:'))
interval = 1#float(input('Enter the interval you want to sample:'))
b = 0#input('Enter the constant in the function:')
m = 1#input('Enter the coefficent of x:')

def tran(x,y):
    x = screenWidth/2 + x
    y = screenHeight/2 - y
    return x,y

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

    # x label
    screen.blit(textX, tran(screenHeight/2 - textRectX.width,0))
    # y label
    screen.blit(textY, tran(0,screenWidth/2))

    # x-axis
    pygame.draw.line(screen,black, tran(-screenWidth/2,0), tran(screenWidth/2,0),1)
    # y-axis
    pygame.draw.line(screen,black, tran(0,screenHeight/2),tran(0,-screenHeight/2),1)

    x = Min
    y = m*x + b
    x2 = x
    y2 =y
        
    while x < Max:
        y = m*x + b
        pygame.draw.line(screen,black, tran(x2,y2) , tran(x,y) ,1)
        x2 = x
        y2 =y
        x = x + interval

running = True
while running:
    event = pygame.event.wait();
    #print(event)
    if event.type == pygame.QUIT:
        running = False

    # clear screen to white
    screen.fill(white)
    render()
    pygame.display.update()
