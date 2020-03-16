#!/usr/bin/python3
import pygame
import math
import sys

class Rect:
    
    def __init__(self, x:float, y:float, width:int, height:int):
        self.__x = float(x)
        self.__y = float(y)
        self.__width = width
        self.__height = height
        self.__pygRect = pygame.Rect(self.__x,self.__y,self.__width,self.__height)
        
    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y, self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self,x):
        self.__x = float(x)
        self.__pygRect.x = self.__x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self,y):
        self.__y = float(y)
        self.__pygRect.y = self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
    
    def colliderect(self,other):
        if self.x+self.width >=other.x and \
            other.x+other.width>=self.x and \
            self.y+self.height >=other.y and \
            other.y+other.height>=self.y:
            return True

    def rectintersection(self,other):
        x5=max(self.x,other.x)
        x6=min(self.x+self.width,other.x+other.width)
        y5=max(self.y,other.y)
        y6=min(self.y+self.height,other.y+other.height)
        if x5>=x6 or y5>=y6:
            return Rect(0,0,0,0)
        return Rect(x5,y5,x6-x5,y6-y5)

    def toPygame(self):
        return self.__pygRect
    
pygame.init()

print ('PyGame Version',pygame.version.ver)
print ('SDL Version', pygame.get_sdl_version())

screenWidth = 800
screenHeight = 800

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)

screen = pygame.display.set_mode((screenWidth, screenHeight))

paddleRectWidth = screenWidth/10
paddleRect = Rect(screenWidth*0.5-paddleRectWidth*0.5,screenHeight*0.9,paddleRectWidth,screenHeight/75)
paddleMoveSpeed = paddleRectWidth/4

ballSize = 20
ballRect = Rect((screenWidth-ballSize)/2,screenHeight/2,ballSize,ballSize)

ystep = 3
xstep = 0
stepStrength = 20.0

points = 0
blocks = []
i = 30

while i<screenWidth-30:
    blocks.append(Rect(i,80,20,20))
    i += 50

def render():
    global ballRect
    global xstep
    global ystep
    screen.fill(white)
    
    ballRect.y += ystep
    ballRect.x += xstep
    print('ball',ballRect,xstep,ystep)

    i = len(blocks)-1
    while i >= 0:
        rect = ballRect.rectintersection(blocks[i])
        if rect.width>0 or rect.height > 0:
            print('block collision',ballRect,blocks[i],rect)
            blocks.pop(i)
            if rect.width > rect.height:
                ystep = -ystep
            else:
                xstep = -xstep
        else:
            pygame.draw.rect(screen,red,blocks[i].toPygame())
        i -=1
        
    if paddleRect.colliderect(ballRect):
        ystep = -ystep
        ballMidPoint = ballRect.x+ballSize/2
        paddleMidPoint = paddleRect.x+paddleRectWidth/2
        xstep += (ballMidPoint - paddleMidPoint)/stepStrength
        print('paddle collision',xstep,ystep)
        
    if ballRect.y + ballSize >  screenHeight:
            running = False
            pygame.quit()
            sys.exit()
            
    if ballRect.y < 0:
        ballRect.y = 0
        ystep = -ystep
        print('top wall',ballRect, ystep)
        
    if ballRect.x< 0:
        ballRect.x = 0
        xstep = -xstep
        print('left wall',ballRect, xstep)
        
    if ballRect.x + ballSize>screenWidth:
        ballRect.x=screenWidth-ballRect.width
        xstep = -xstep
        print('right wall',ballRect, xstep)

    pygame.draw.rect(screen,black,paddleRect.toPygame())
    pygame.draw.rect(screen,black,ballRect.toPygame())

    pygame.display.update()

running = True
pygame.key.set_repeat(50, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RIGHT:
                    paddleRect.x=min(paddleRect.x + paddleMoveSpeed,screenWidth - paddleRectWidth)
            if event.key == pygame.K_LEFT:
                    paddleRect.x=max(paddleRect.x - paddleMoveSpeed, 0)
        elif event.type == pygame.MOUSEMOTION:
            paddleRect.x = min(max(pygame.mouse.get_pos()[0] - paddleRectWidth*0.5, 0),screenWidth-paddleRectWidth)

    render()
