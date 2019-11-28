#!/usr/bin/python

import pygame
import math

def compute_y(x):
    return x

black = [0, 0, 0]
red = [255, 0, 0]
gray = [127, 127, 127]
white = [255, 255, 255]
lightGray = [180, 180, 180]

graphColor = black
axisColor = gray
traceColor = red
gridColor = lightGray

screenWidth = 800
screenHeight = 800

graphWidth = initialWidth = float(20)
graphHeight = initialHeight = float(20)

graphCenterX = float(0)
graphCenterY = float(0)

sx = screenWidth / float(graphWidth)
sy = screenHeight / float(graphHeight)

interval = 1 / sx
moveIncrement = interval * 16
traceIncrement = (graphWidth/initialWidth)/4
zoomFactor = 2

MinX = -graphWidth/2 + graphCenterX
MaxX = graphWidth/2 + graphCenterX
MinY = -graphHeight/2 + graphCenterY
MaxY = graphHeight/2 + graphCenterY

pygame.init()
pygame.font.init()
pygame.display.set_caption('Graph')

font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))

textX = font.render('X', True, black, white)
textY = font.render('Y', True, black, white)

traceX = graphCenterX
traceY = compute_y(traceX)
coordinates = str((traceX, traceY))
textPos = font.render(coordinates, True, black, white)

def tran(x, y):

    # translate
    x = x - graphCenterX
    y = y - graphCenterY

    # scale
    x = x * sx
    y = y * sy

    # transform to screen coordinates
    x = screenWidth/2 + x
    y = screenHeight/2 - y

    return int(x), int(y)


def render():
    print("render")
    global sx
    global sy
    global moveIncrement
    global traceIncrement

    screen.fill(white)
    sx = screenWidth / float(graphWidth)
    sy = screenHeight / float(graphHeight)
    textXWidth = textX.get_width() / sx

    interval = 1 / sx
    moveIncrement = interval * 16
    traceIncrement = (graphWidth/initialWidth)/4

    MinX = -graphWidth/2 + graphCenterX
    MaxX = graphWidth/2 + graphCenterX
    MinY = -graphHeight/2 + graphCenterY
    MaxY = graphHeight/2 + graphCenterY

    # x label
    screen.blit(textX, tran(MaxX - textXWidth, 0))
    # y label
    screen.blit(textY, tran(0, MaxY))

    print("gridExp",
          graphWidth,
          math.log(graphWidth,10),
          math.floor(math.log(graphWidth,10))-1)
    
    gridExp = math.floor(math.log(graphWidth,10))-1
    gridFactor = math.pow(10,gridExp)

    print("gridFactor",gridExp,gridFactor)
    
    # vertical grid lines
    gridX = round(MinX/gridFactor, 0) * gridFactor
    while gridX < MaxX:
        #print("gridX",gridX,MinY,MaxY)
        pygame.draw.line(screen, gridColor, tran(
            gridX, MinY), tran(gridX, MaxY), 1)
        gridX = gridX + gridFactor

    # horizontal grid lines
    gridY = round(MinY/gridFactor, 0) * gridFactor
    while gridY < MaxY:
        pygame.draw.line(screen, gridColor, tran(
            MinX, gridY), tran(MaxX, gridY), 1)
        gridY = gridY + gridFactor

    # x-axis
    pygame.draw.line(screen, axisColor, tran(MinX, 0), tran(MaxX, 0), 1)
    # y-axis
    pygame.draw.line(screen, axisColor, tran(0, MinY), tran(0, MaxY), 1)

    # trace mode - prints position
    coordinates = str((round(traceX, 4), round(traceY, 4)))
    textPos = font.render(coordinates, True, black, white)
    textTraceWidth = textPos.get_width() / sx
    textTraceHeight = textPos.get_height() / sx
    textTrace = MaxX - textTraceWidth
    screen.blit(textPos, tran(textTrace, MaxY))
    # prints zoom amount
    zoomAmount = graphWidth/initialWidth
    textZoom = font.render(
        'Zoom: '+str(zoomAmount), True, black, white)
    textZoomWidth = textZoom.get_width() / sx
    textZoomX = MaxX - textZoomWidth
    textZoomY = MaxY - textTraceHeight
    screen.blit(textZoom, tran(textZoomX, textZoomY))

    # draw function
    x = MinX
    y = compute_y(x)
    x2 = x
    y2 = y

    while x < MaxX:
        y = compute_y(x)
        pygame.draw.line(screen, graphColor, tran(x2, y2), tran(x, y), 2)
        x2 = x
        y2 = y
        x = x + interval

    # trace circle
    pygame.draw.circle(screen, traceColor, tran(traceX, traceY), 5)

    pygame.display.update()


running = True
pygame.key.set_repeat(75, 50)
while running:
    event = pygame.event.wait()
    # print('event',event)
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            graphCenterY = graphCenterY - moveIncrement
        if event.key == pygame.K_w:
            graphCenterY = graphCenterY + moveIncrement
        if event.key == pygame.K_a:
            graphCenterX = graphCenterX - moveIncrement
        if event.key == pygame.K_d:
            graphCenterX = graphCenterX + moveIncrement
        if event.key == pygame.K_EQUALS:
            graphWidth = graphWidth * zoomFactor
            graphHeight = graphHeight * zoomFactor
        if event.key == pygame.K_MINUS:
            graphWidth = graphWidth / zoomFactor
            graphHeight = graphHeight / zoomFactor
        if event.key == pygame.K_LEFT:
            traceX = traceX - traceIncrement
            traceY = compute_y(traceX)
        if event.key == pygame.K_RIGHT:
            traceX = traceX + traceIncrement
            traceY = compute_y(traceX)
        if event.key == pygame.K_SPACE:
            graphCenterX = traceX
            graphCenterY = traceY
        if event.key == pygame.K_r:
            graphWidth = initialWidth
            graphHeight = initialHeight
            graphCenterX = graphCenterY = 0
            traceX = 0
            traceY = compute_y(0)

    render()
