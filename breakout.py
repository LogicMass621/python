#!/usr/bin/python3
import pygame
import math
import sys

class Rect:
    
    def __init__(self, x:float, y:float, width:int, height:int):
        self.__x = x
        self.__y = y
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

class Screen:

    def render(self):
        return

    def handleEvent(self,event):
        return

pygame.init()
pygame.font.init()

print ('PyGame Version',pygame.version.ver)
print ('SDL Version', pygame.get_sdl_version())

screenWidth = 800
screenHeight = 800

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,7,58)
green = (50,255,50)
teal =(0,255,255)

pygame.display.set_caption('Breakout!')

surface = pygame.display.set_mode((screenWidth, screenHeight))

screens = []

class StartScreen(Screen):
    largeFont = pygame.font.Font('freesansbold.ttf', 80)
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    textBreakout = largeFont.render('BREAKOUT',True,teal,black)
    textBreakoutX=screenWidth/2-textBreakout.get_width()/2
    textBreakoutY=screenHeight/3

    textStart=font.render('Press SPACE to start',True,teal,black)
    textStartX=screenWidth/2-textStart.get_width()/2
    textStartY=screenHeight/2-textStart.get_height()/2

    def render(self):
            surface.fill(black)

            surface.blit(self.textBreakout,(self.textBreakoutX,self.textBreakoutY))
            surface.blit(self.textStart,(self.textStartX,self.textStartY))
            
            pygame.display.update()
            return True

    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screens.append(GameScreen())
        return True

class EndScreen(Screen):

    font = pygame.font.Font('freesansbold.ttf', 20)
    
    def render(self):
        surface.fill(black)
        textGameover= self.font.render('GAMEOVER!', True, red, black)
        textGameoverX=screenWidth/2-textGameover.get_width()/2
        textGameoverY=screenHeight/2-textGameover.get_height()/2
        surface.blit(textGameover,(textGameoverX,textGameoverY))
        pygame.display.update()

    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screens.pop()
        return True
        
class GameScreen(Screen):
    
    font = pygame.font.Font('freesansbold.ttf', 20)
    largeFont = pygame.font.Font('freesansbold.ttf', 60)

    paddleRectWidth = screenWidth/10
    paddleRect = Rect(screenWidth*0.5-paddleRectWidth*0.5,screenHeight*0.9,paddleRectWidth,screenHeight/75)
    paddleMoveSpeed = paddleRectWidth/4

    ballSize = 20

    ystep = 3
    xstep = 0
    stepStrength = 20.0
 
    points = 0

    def __init__(self):    
        self.ballRect = Rect((screenWidth-self.ballSize)/2,screenHeight/2,self.ballSize,self.ballSize)

        self.blocks = []
        i = 30
        while i<screenWidth-30:
            self.blocks.append(Rect(i,80,20,20))
            i += 50

    def render(self):

        surface.fill(black)

        i = len(self.blocks)-1
        if i == -1:
            screens.pop()
            screens.push(EndScreen())
            return True
    
        self.ballRect.y += self.ystep
        self.ballRect.x += self.xstep
        
        while i >= 0:
            rect = self.ballRect.rectintersection(self.blocks[i])
            if rect.width>0 or rect.height > 0:
                self.blocks.pop(i)
                self.points+=10
                if rect.width > rect.height:
                    self.ystep = -self.ystep
                else:
                    self.xstep = -self.xstep
            else:
                pygame.draw.rect(surface,red,self.blocks[i].toPygame())
            i -=1

        textScore = self.font.render('Score: '+str(self.points)+' ', True, black, white)
        textScoreX=screenWidth-textScore.get_width()
        textScoreY=textScore.get_height()/3
        surface.blit(textScore,(textScoreX,textScoreY))
        
        if self.paddleRect.colliderect(self.ballRect):
            self.ystep = -self.ystep
            ballMidPoint = self.ballRect.x+self.ballSize/2
            paddleMidPoint = self.paddleRect.x+self.paddleRectWidth/2
            self.xstep += (ballMidPoint - paddleMidPoint)/self.stepStrength
            
        if self.ballRect.y + self.ballSize >  screenHeight:
                screens.pop()
                return False
                
        if self.ballRect.y < 0:
            self.ballRect.y = 0
            self.ystep = -self.ystep
            
        if self.ballRect.x< 0:
            self.ballRect.x = 0
            self.xstep = -self.xstep
            
        if self.ballRect.x + self.ballSize>screenWidth:
            self.ballRect.x=screenWidth-self.ballRect.width
            self.xstep = -self.xstep

        pygame.draw.rect(surface,teal,self.paddleRect.toPygame())
        pygame.draw.rect(surface,green,self.ballRect.toPygame())

        pygame.display.update()
        return True

    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                        self.paddleRect.x=min(self.paddleRect.x + self.paddleMoveSpeed,screenWidth - self.paddleRectWidth)
            if event.key == pygame.K_LEFT:
                        self.paddleRect.x=max(self.paddleRect.x - self.paddleMoveSpeed, 0)
        elif event.type == pygame.MOUSEMOTION:
            self.paddleRect.x = min(max(pygame.mouse.get_pos()[0] - self.paddleRectWidth*0.5, 0),
                               screenWidth-self.paddleRectWidth)
        return True

pygame.key.set_repeat(50, 0)
screens.append(StartScreen())

while True:
    if not screens:
        break
    screen = screens[-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
                
        screen.handleEvent(event)
        
    screen.render()

pygame.quit()
sys.exit()
