#!/usr/bin/python3
import pygame
import threading
import socket

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

p1X = 20
p1Y=175
p2X=360
p2Y=175
paddleWidth=20
paddleHeight = 50
p1Rect = Rect(p1X,p1Y,paddleWidth,paddleHeight)
p2Rect = Rect(p2X,p2Y,paddleWidth,paddleHeight)

x=socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hostName = socket.gethostname()
port=8080
running = True

try:
    x.bind((hostName,port))
    x.listen(1)
    conn,addr=x.accept()
    thisUser=p1Rect
    otherUser=p2Rect
except OSError:
    x.connect(('massimo-pc',port))
    conn=x
    thisUser=p2Rect
    otherUser=p1Rect
    
black=(0,0,0)
white=(255,255,255)
screenWidth=400
screenHeight=400
screen = pygame.display.set_mode((screenWidth, screenHeight))


def receive():
    global otherUserY
    global userY
    while running:
        recv_msg=conn.recv(1024)
        recv_msg=recv_msg.decode()
        print('recv_msg',recv_msg)
        if recv_msg=='up':
            otherUser.y-=10
        if recv_msg=='down':
            otherUser.y+=10
            
def eventLoop():
    global running
    global userY
    global otherUserY
    pygame.display.init()
    while running:
        event=pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print('Keydown')
            if event.key == pygame.K_UP:
                print(event)
                thisUser.y-=10
                send_msg='up'.encode()
                conn.send(send_msg)
            if event.key == pygame.K_DOWN:
                print(event)
                thisUser.y+=10
                send_msg='down'.encode()
                conn.send(send_msg)

                    
def render():
    screen.fill(white)

    pygame.draw.rect(screen,black,p1Rect.toPygame())
    pygame.draw.rect(screen,black,p2Rect.toPygame())
    pygame.display.update()

recv_thread = threading.Thread(target=receive)
recv_thread.start()
print('receive loop start')

event_thread = threading.Thread(target=eventLoop)
event_thread.start()
print('eventLoop start')

while running:
    render()
