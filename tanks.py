#!/usr/bin/python3
import pygame
import threading
import sys
import socket
import time
import math

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

class Int:

    def __init__(self, n: int):
        self.n = n

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

x=socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hostName = socket.gethostname()
port=50000
server_IP = '192.168.1.160'

black=(0,0,0)
white=(255,255,255)

screenWidth=400
screenHeight=400
screen = pygame.display.set_mode((screenWidth, screenHeight))

tankSize= 30
tank = pygame.image.load('tank.png')
p1Rect=Rect(screenWidth-4*tankSize,(screenHeight-tankSize)/2,tankSize,tankSize)
p2Rect=Rect(3*tankSize,(screenHeight-tankSize)/2,tankSize,tankSize)
p1Angle = Int(0)
p2Angle = Int(0)

running=True
singlePlayer = True

tanks = {}
tanks[0] = tank
step = 15
for i in range(step, 359, step):
    print("adding tank", i)
    tanks[i] = rot_center(tank,-i)

print(tanks)

if singlePlayer != True:
    server = input('Do you want to start the server?')
    if server.count('y'or'Y'):
        x.bind((hostName,port))
        print("Bound to address ",x.getsockname())
        x.listen(1)
        conn,addr=x.accept()
        thisUser=p1Rect
        otherUser=p2Rect
        pygame.display.set_caption('Player One')
        firstPlayer = True
    else:

        server_IP=input("Server IP:")
        if server_IP == 'Massi':
            x.connect(('192.168.1.160',port))
        else: 
            x.connect((server_IP,port))
        conn=x
        thisUser=p2Rect
        otherUser=p1Rect
        pygame.display.set_caption('Player Two')
        firstPlayer = False
else:
    thisUser = p1Rect
    otherUser = p2Rect
    thisAngle = p1Angle
    otherAngle = p2Angle


clock=pygame.time.Clock()

def receive():
    global thisUser,otherUser
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






                new_msg=True
                msg_buffer=msg_buffer[headerSize+msglen:]
                #print('new buffer',msg_buffer)

def eventLoop():
    global running, thisUser, otherUser, thisAngle, otherAngle
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

            if event.key == pygame.K_w:
                radians = math.radians(thisAngle.n)
                thisUser.x += 10*math.sin(radians)
                thisUser.y -= 10*math.cos(radians)
                if singlePlayer != True:
                    msg=f'paddle:{thisUser.x}:{thisUser.y}'.encode()
                    conn.send(msg)

            if event.key == pygame.K_s:
                radians = math.radians(thisAngle.n)
                thisUser.x -= 10*math.sin(radians)
                thisUser.y += 10*math.cos(radians)
                if singlePlayer != True:
                    msg=f'paddle:{thisUser.x}:{thisUser.y}'.encode()
                    conn.send(msg)

            if event.key == pygame.K_d:
                thisAngle.n = (thisAngle.n + 15) % 360
                print("thisAngle",thisAngle.n)
                if singlePlayer != True:
                    msg=f'paddle:{thisUser.x}:{thisUser.y}'.encode()
                    conn.send(msg)

            if event.key == pygame.K_a:
                thisAngle.n = (thisAngle.n - 15) % 360
                print("thisAngle",thisAngle.n)
                if singlePlayer != True:
                    msg=f'paddle:{thisUser.x}:{thisUser.y}'.encode()
                    conn.send(msg)
        time.sleep(0.001)


def render():
    screen.fill(white)
    screen.blit(tanks[p1Angle.n],p1Rect.toPygame())
    screen.blit(tanks[p2Angle.n],p2Rect.toPygame())
    pygame.display.update()

event_thread = threading.Thread(target=eventLoop)
event_thread.start()
if singlePlayer != True:
    recv_thread = threading.Thread(target=receive)
    recv_thread.start()

while running:
    render()

sys.exit()
pygame.quit()