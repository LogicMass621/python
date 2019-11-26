#!/usr/bin/python

import pygame, math

def compute_y(x):
   return 2*x + 5

black = [0, 0, 0]
white = [255, 255, 255]

screenWidth = 800
screenHeight = 800

graphWidth = 100
graphHeight = 100

graphCenterX = 0
graphCenterY = 0

sx= screenWidth / float(graphWidth)
sy= screenHeight / float(graphHeight)

interval = 1 / sx
step = interval*3

pygame.init()
pygame.font.init()
pygame.display.set_caption('Graph')

font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))

textX = font.render('X', True, black, white)
textY = font.render('Y', True, black, white)

textXWidth = textX.get_width() / sx

traceX = graphCenterX
traceY = compute_y(traceX)
coordinates = str((traceX,traceY))
textPos = font.render(coordinates,True,black,white)

def tran(x,y):

    # translate
    x = x - graphCenterX
    y = y - graphCenterY
    
    # scale
    x = x * sx
    y = y * sy

    # transform to screen coordinates
    x = screenWidth/2 + x
    y = screenHeight/2 - y
    
    return int(x),int(y)

def render():
    
    global MinX
    global MaxX
    global MinY
    global MaxY
    global sx
    global sy
    global graphWidth
    global graphHeight
    global interval

    
    sx= screenWidth / float(graphWidth)
    sy= screenHeight / float(graphHeight)
    textXWidth = textX.get_width() / sx
    
    MinX = -graphWidth/2 + graphCenterX
    MaxX = graphWidth/2 + graphCenterX
    MinY = -graphHeight/2 + graphCenterY
    MaxY = graphHeight/2 + graphCenterY

    interval = 1 / sx
    step = interval*3

    # x label
    screen.blit(textX, tran(MaxX - textXWidth,0))
    # y label
    screen.blit(textY, tran(0,MaxY))
    #trace mode - prints position
    coordinates = str((round(traceX,2),round(traceY,2)))
    textPos = font.render(coordinates,True,black,white)
    textTraceWidth = textPos.get_width() / sx
    textTraceHeight = textPos.get_height() / sx
    textTrace = MaxX - textTraceWidth
    screen.blit(textPos,tran(textTrace,MaxY))
    #prints zoom amount
    zoomAmount = graphWidth/100
    textZoom = font.render('Zoom: '+str(round(zoomAmount,2)),True,black,white)
    textZoomWidth = textZoom.get_width() / sx
    textZoomX = MaxX - textZoomWidth
    textZoomY = MaxY - textTraceHeight
    screen.blit(textZoom,tran(textZoomX,textZoomY))

    # x-axis
    pygame.draw.line(screen,black, tran(MinX,0), tran(MaxX,0),1)
    # y-axis
    pygame.draw.line(screen,black, tran(0,MinY),tran(0,MaxY),1)

    pygame.draw.circle(screen,black,tran(traceX,traceY),5)

    x = MinX
    y = compute_y(x)
    x2 = x
    y2 = y
        
    while x < MaxX:
        y = compute_y(x)
        pygame.draw.line(screen,black, tran(x2,y2) , tran(x,y) ,1)
        x2 = x
        y2 = y
        x = x + interval

running = True
pygame.key.set_repeat(75,50)
while running:
    event = pygame.event.wait();
    #print('event',event)
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            graphCenterY = graphCenterY - step*graphWidth/50
        if event.key == pygame.K_w:
           graphCenterY = graphCenterY + step*graphWidth/50
        if event.key == pygame.K_a:
            graphCenterX = graphCenterX - step*graphWidth/50
        if event.key == pygame.K_d:
            graphCenterX = graphCenterX + step*graphWidth/50
        if event.key == pygame.K_EQUALS:
            graphWidth = graphWidth * step
            graphHeight = graphHeight * step
        if event.key == pygame.K_MINUS:
            graphWidth = graphWidth / step
            graphHeight = graphHeight / step
        if event.key == pygame.K_LEFT:
            global self
            traceX = traceX - 1*graphWidth/100
            traceY = compute_y(traceX)
        if event.key == pygame.K_RIGHT:
            global self
            traceX = traceX + 1*graphWidth/100
            traceY = compute_y(traceX)

    # clear screen to white
    screen.fill(white)
    render()
    pygame.display.update()
