#!/usr/bin/python3
import pygame
import threading
import socket
import math
import sys
import time
import random

class Rect:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(
            self.__x, self.__y, self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y,
                                                         self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)
        self.__pyg_rect.x = self.__x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)
        self.__pyg_rect.y = self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def colliderect(self, other):
        if self.x+self.width >= other.x and \
                other.x+other.width >= self.x and \
                self.y+self.height >= other.y and \
                other.y+other.height >= self.y:
            return True

    def rectintersection(self, other):
        x5 = max(self.x, other.x)
        x6 = min(self.x+self.width, other.x+other.width)
        y5 = max(self.y, other.y)
        y6 = min(self.y+self.height, other.y+other.height)
        if x5 >= x6 or y5 >= y6:
            return Rect(0, 0, 0, 0)
        return Rect(x5, y5, x6-x5, y6-y5)

    def toPygame(self):
        return self.__pyg_rect
    
black=(0,0,0)
white=(255,255,255)
screenWidth=400
screenHeight=400
screen = pygame.display.set_mode((screenWidth, screenHeight))

paddleWidth=20
paddleHeight = 60

p1Rect = Rect(paddleWidth,(screenHeight-paddleHeight)/2,
              paddleWidth,paddleHeight)
p2Rect = Rect(screenWidth-2*paddleWidth,(screenHeight-paddleHeight)/2,
              paddleWidth,paddleHeight)

ballSize=20
ballRect = Rect((screenHeight-ballSize)/2,(screenWidth-ballSize)/2,ballSize,ballSize)
speed=2
ballXStep=speed
ballYStep=0
stepStrength=30.0

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)
p1Score=0
p2Score=0
maxScore=5
textP1Score=font.render('Player 1:'+str(p1Score),True,black)
textP2Score=font.render("Player 2:"+str(p2Score),True,black)
textGameOver=font.render('Game Over!',True,black)
movePaddle = 0
paddleDelay=0

running = True
delayTime=3
thisUser=p1Rect
otherUser=p2Rect
clock=pygame.time.Clock()

            
def eventLoop():
    global running, userY, otherUserY, counter
    pygame.key.set_repeat(75 , 50)
    pygame.display.init()
    while running:
        event=pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running = False
                    sys.exit()
                    pygame.quit()
                if event.key == pygame.K_UP:
                    if thisUser.y != 0:
                        thisUser.y-=10
                if event.key == pygame.K_DOWN:
                    if thisUser.y != screenHeight-paddleHeight:
                        thisUser.y+=10
        
def ball():
    global ballXStep, ballYStep, ballRect, counter,running
    global p1Score,p2Score,thisUser,otherUser
    global textP1Score,textP2Score,texGameOver
    global movePaddle, paddleDelay

    time.sleep(delayTime)

    while running:
        if thisUser.colliderect(ballRect):
            ballMidPoint = ballRect.y+ballSize/2
            paddleMidPoint = thisUser.y+paddleHeight/2
            ballYStep += (ballMidPoint - paddleMidPoint)/stepStrength
            ballYStep = max(-speed+.25,min(speed-.25, ballYStep))
            ballXStep = math.sqrt(abs(speed*speed - ballYStep*ballYStep))
            if ballXStep*ballXStep+ballYStep*ballYStep>speed*speed:
                print('thisUser.x: ',thisUser.x,' ballXStep: ',ballXStep,
                      'ballYStep: ',ballYStep,' ballRect.x: ',ballRect.x,' ballRect.y: ',ballRect.y,
                      'X*X+Y*Y=',ballXStep*ballXStep+ballYStep*ballYStep,'speed^2',speed*speed,
                      'collideThisUser')

        if otherUser.colliderect(ballRect):
            ballMidPoint = ballRect.y+ballSize/2
            paddleMidPoint = otherUser.y+paddleHeight/2
            ballYStep += (ballMidPoint - paddleMidPoint)/stepStrength
            ballYStep = max(-speed+.25,min(speed-.25, ballYStep))
            ballXStep = - \
                math.sqrt(abs(speed*speed - ballYStep*ballYStep))
            if ballXStep*ballXStep+ballYStep*ballYStep>speed*speed:
                print('otherUser.x: ',thisUser.x,
                      ' ballXStep: ',ballXStep,'ballYStep: ',ballYStep,
                      ' ballRect.x: ',ballRect.x,' ballRect.y: ',ballRect.y,
                      'X*X+Y*Y=',ballXStep*ballXStep+ballYStep*ballYStep,'speed^2',speed*speed,
                       'collideOtherUser')
                
        if ballRect.x+ballSize>screenWidth:

            p1Score+=1
            textP1Score=font.render('Player 1:'
                                          +str(p1Score),True,black)
                        
            ballRect.x=200-ballSize/2
            ballRect.y=200-ballSize/2
            ballXStep=speed
            ballYStep=0
            thisUser.y=(screenHeight-paddleHeight)/2
            otherUser.y=(screenHeight-paddleHeight)/2

            time.sleep(delayTime)
            
            if p1Score==maxScore:
                p1Score=0
                textP1Score=font.render('Player 1:'
                                              +str(p1Score),True,black)
                
        if ballRect.x<0:

            p2Score+=1
            textP2Score=font.render("Player 2:"
                                           +str(p2Score),True,black)
                        
            ballRect.x=200-ballSize/2
            ballRect.y=200-ballSize/2
            ballXStep=-speed
            thisUser.y=(screenHeight-paddleHeight)/2
            otherUser.y=(screenHeight-paddleHeight)/2
            ballYStep=0

            time.sleep(delayTime)
            
            if p2Score==maxScore:
                p2Score=0
                textP2Score=font.render("Player 2:"
                                               +str(p2Score),True,black)
                
        if ballRect.y<0:
            ballRect.y=0
            ballYStep=-ballYStep
            paddleDelay=-random.randint(40,57)
            print(paddleDelay)
        if ballRect.y+ballSize>screenHeight:
            ballRect.y=screenHeight-ballSize
            ballYStep=-ballYStep
            paddleDelay=-random.randint(40,55)
            print(paddleDelay)
        if movePaddle%5==0 and paddleDelay>=1:
            if p2Rect.y+paddleHeight < ballRect.y:
                p2Rect.y += 10
            if p2Rect.y > ballRect.y:
                p2Rect.y -= 10
        movePaddle+=1
        paddleDelay+=1
            
        ballRect.x+=ballXStep
        ballRect.y+=ballYStep

        time.sleep(.01)

                    
def render():
    screen.fill(white)
    
    pygame.draw.rect(screen,black,p1Rect.toPygame())
    pygame.draw.rect(screen,black,p2Rect.toPygame())
    pygame.draw.rect(screen,black,ballRect.toPygame())
    screen.blit(textP1Score,(0,0))
    screen.blit(textP2Score,(screenWidth-textP2Score.get_width(),0))

    if p1Score==maxScore or p2Score==maxScore:
        screen.blit(textGameOver,(screenWidth/2-textGameOver.get_width()/2,
                                screenHeight/2-textGameOver.get_height()*2))

    pygame.display.update()


event_thread = threading.Thread(target=eventLoop)
event_thread.start()
ball_thread = threading.Thread(target=ball)
ball_thread.start()

while running: 
    render()
    clock.tick(60)
    #print(clock.get_fps())


