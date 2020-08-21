#!/usr/bin/python3
import pygame
import threading
import socket
import math
import sys
import time

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
speed=1
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
headerSize=10
running = True
delayTime=3
x=socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hostName = socket.gethostname()
port=50000
running=True
ballUpdate = False
ball_reset=False
server_IP = '192.168.1.160'

try:
    x.bind((hostName,port))
    print("Bound to address ",x.getsockname())
    x.listen(1)
    conn,addr=x.accept()
    thisUser=p1Rect
    otherUser=p2Rect
    pygame.display.set_caption('Player One')
    firstPlayer = True
except OSError:
    server_IP=input("Server IP:")
    x.connect((server_IP,port))
    conn=x
    thisUser=p2Rect
    otherUser=p1Rect
    pygame.display.set_caption('Player Two')
    firstPlayer = False

clock=pygame.time.Clock()

def receive():
    global ballRect, ballYStep,ballXStep, p1Score,p2Score,textP1Score,textP2Score,thisUser,otherUser
    global running
    while running:
        msg_buffer = b''
        new_msg=True
        while True:

            if (new_msg and len(msg_buffer) < headerSize) or (not new_msg and len(msg_buffer) < headerSize+msglen):
                msg = conn.recv(16)
                msg_buffer += msg
                #print('recv',msg, 'buffer', msg_buffer)

            if new_msg:
                #print(f"new msg len:",msg_buffer[:headerSize].decode())
                msglen=int(msg_buffer[:headerSize])
                new_msg=False

            if len(msg_buffer)-headerSize>=msglen: # full message
                decoded_msg=msg_buffer[headerSize:headerSize+msglen].decode()
                #print('decoded_msg_received',decoded_msg)
                if decoded_msg.count('ball'):
                    x=decoded_msg.split(':')
                    x_coord=x[1]
                    y_coord=x[2]
                    ballRect.x=float(x_coord)
                    ballRect.y=float(y_coord)                   
                    #print('ball coords',x_coord,y_coord)
                if decoded_msg.count('paddle'):
                    x=decoded_msg.split(':')
                    otherUser.y=x[1]
                if decoded_msg.count('reset'):
                    scores=decoded_msg.split(':')
                    p1Score=scores[1]
                    p2Score=scores[2]
                    textP1Score=font.render('Player 1:'
                        +str(p1Score),True,black)
                    textP2Score=font.render("Player 2:"
                        +str(p2Score),True,black)

                new_msg=True
                msg_buffer=msg_buffer[headerSize+msglen:]
                #print('new buffer',msg_buffer)


def eventLoop():
    global running, thisUser, otherUser, counter, ballUpdate, ball_reset, ballRect
    pygame.key.set_repeat(75 , 50)
    pygame.display.init()
    while running:
        event=pygame.event.poll()

        if event.type == pygame.QUIT:
        	# TODO send quit to client
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key==pygame.K_ESCAPE:
            	# TODO send quit to client
                running = False

            if event.key == pygame.K_UP:
                if thisUser.y != 0:
                    thisUser.y-=10
                    msg=f'paddle:{thisUser.y}'.encode()
                    msg = bytes(f'{len(msg):<{headerSize}}','utf-8')+msg
                    conn.send(msg)

            if event.key == pygame.K_DOWN:
                if thisUser.y != screenHeight-paddleHeight:
                    thisUser.y+=10
                    msg=f'paddle:{thisUser.y}'.encode()
                    msg = bytes(f'{len(msg):<{headerSize}}','utf-8')+msg
                    conn.send(msg)
        if ball_reset == True:
            msg =f'reset:{p1Score}:{p2Score}'.encode()
            msg = bytes(f'{len(msg):<{headerSize}}','utf-8')+msg
            conn.send(msg)
            ball_reset=False
        
        if ballUpdate==True:
            msg = f'ball:{ballRect.x}:{ballRect.y}'.encode()
            msg = bytes(f'{len(msg):<{headerSize}}','utf-8')+ msg
            conn.send(msg)
            ballUpdate=False

        time.sleep(0.001)

def ballReset():

    global p1Score,textP1Score,p2Score,textP2Score
    global ballRect,speed,p1Rect,p2Rect
    global ballXStep,ballYStep, ballUpdate, ball_reset
    #print('ballReset')
    ball_reset=True
    ballRect.x=200-ballSize/2
    ballRect.y=200-ballSize/2
    ballXStep=0
    ballYStep=0
    ballUpdate=True
    time.sleep(delayTime)
    textP1Score=font.render('Player 1:'
        +str(p1Score),True,black)
    textP2Score=font.render("Player 2:"
        +str(p2Score),True,black)
    ballXStep=speed

def ball():
    global ballXStep, ballYStep, ballRect, counter,running
    global p1Score,p2Score,thisUser,otherUser
    global textP1Score,textP2Score,texGameOver
    global movePaddle, paddleDelay, ballUpdate

    time.sleep(delayTime)

    while running:
        if thisUser.colliderect(ballRect):
            ballMidPoint = ballRect.y+ballSize/2
            paddleMidPoint = thisUser.y+paddleHeight/2
            ballYStep += (ballMidPoint - paddleMidPoint)/stepStrength
            ballYStep = max(-speed+.25,min(speed-.25, ballYStep))
            ballXStep = math.sqrt(abs(speed*speed - ballYStep*ballYStep))
            #if ballXStep*ballXStep+ballYStep*ballYStep>speed*speed:
                #print('thisUser.x: ',thisUser.x,' ballXStep: ',ballXStep,
                      #'ballYStep: ',ballYStep,' ballRect.x: ',ballRect.x,' ballRect.y: ',ballRect.y,
                      #'X*X+Y*Y=',ballXStep*ballXStep+ballYStep*ballYStep,'speed^2',speed*speed,
                      #'collideThisUser')

        if otherUser.colliderect(ballRect):
            ballMidPoint = ballRect.y+ballSize/2
            paddleMidPoint = otherUser.y+paddleHeight/2
            ballYStep += (ballMidPoint - paddleMidPoint)/stepStrength
            ballYStep = max(-speed+.25,min(speed-.25, ballYStep))
            ballXStep = - \
                math.sqrt(abs(speed*speed - ballYStep*ballYStep))
            #if ballXStep*ballXStep+ballYStep*ballYStep>speed*speed:
                #print('otherUser.x: ',thisUser.x,
                      #' ballXStep: ',ballXStep,'ballYStep: ',ballYStep,
                      #' ballRect.x: ',ballRect.x,' ballRect.y: ',ballRect.y,
                      #'X*X+Y*Y=',ballXStep*ballXStep+ballYStep*ballYStep,'speed^2',speed*speed,
                       #'collideOtherUser')
                
        if ballRect.x+ballSize>screenWidth:
            p1Score+=1
            ballReset()
        if ballRect.x<0:
            p2Score+=1
            ballReset()
        if ballRect.y<0:
            ballRect.y=0
            ballYStep=-ballYStep
        if ballRect.y+ballSize>screenHeight:
            ballRect.y=screenHeight-ballSize
            ballYStep=-ballYStep

        ballRect.x+=ballXStep
        ballRect.y+=ballYStep
        ballUpdate=True

        time.sleep(0.005)

                    
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
        running=False

    pygame.display.update()


event_thread = threading.Thread(target=eventLoop)
event_thread.start()

recv_thread = threading.Thread(target=receive)
recv_thread.start()

if firstPlayer==True:
    ball_thread = threading.Thread(target=ball)
    ball_thread.start()

while running: 
    render()
    clock.tick(60)
    #print(clock.get_fps())

sys.exit()
pygame.quit()
