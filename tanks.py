#!/usr/bin/python3
import pygame
import threading
import sys
import socket
import time
import math
import statistics

class Rect:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(
            int(self.__x), int(self.__y), self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y,
            self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)
        self.__pyg_rect.x = int(self.__x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)
        self.__pyg_rect.y = int(self.__y)

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
        else:
            return False

    def colliderect(self, other, adjustment):
        x=other.x+adjustment
        y=other.y+adjustment
        width=other.width-adjustment*2
        height=other.height-adjustment*2
        if self.x + self.width >= x and \
                x+width >= self.x and \
                self.y + self.height >= y and \
                y+height >= self.y:
            return True
        else:
            return False

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

# global unique identifier
class Guid:

    def __init__(self):
        self.__id = 0

    def nextId(self):
        self.__id += 1
        return self.__id

guid = Guid()

class Projectile:

    def __init__(self, Id, xStep: float, yStep: float, rect, player):
        self.__xStep = xStep
        self.__yStep = yStep
        self.__rect = rect
        self.__player = player
        self.__Id = Id


    def __str__(self):
        return 'xStep: {} yStep: {} rect: {} player: {}'.format(self.__xStep,
            self.__yStep, self.__rect, self.__player)

    @property
    def xStep(self):
        return self.__xStep
    @xStep.setter
    def xStep(self, xStep):
        self.__xStep = float(xStep)
    @property
    def yStep(self):
        return self.__yStep
    @yStep.setter
    def yStep(self, yStep):
        self.__yStep = float(yStep)
    @property
    def rect(self):
        return self.__rect
    @rect.setter
    def rect(self, rect):
        self.__rect = rect
    @property
    def player(self):
        return self.__player
    @property
    def Id(self):
        return self.__Id
    @Id.setter
    def Id(self, Id):
        self.__Id=int(Id)

    def collideRect(self,other,adjustment):
        if other.player!=int(self.player):
            return self.rect.colliderect(other.rect,adjustment)
        else:
            return False

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Tank:
    def __init__(self, player, rect, angle, lives):
        self.__rect = rect
        self.__angle = angle
        self.__lastFired = 0
        self.__lives = lives
        self.__player=player



    @property
    def rect(self):
        return self.__rect
    @property
    def angle(self):
        return self.__angle
    @property
    def lastFired(self):
        return self.__lastFired
    @property
    def lives(self):
        return self.__lives
    @property
    def player(self):
        return self.__player
    @property
    def lives(self):
        return self.__lives
    

    @rect.setter
    def rect(self,rect):
        self.__rect = rect
    @angle.setter
    def angle(self,angle):
        self.__angle = angle
    @lastFired.setter
    def lastFired(self, time):
        self.__lastFired = time
    @player.setter
    def player(self,player):
        self.__player = player
    @lives.setter
    def lives(self, lives):
        self.__lives = lives
    def reduceLife(self):
        self.__lives -= 1


x = socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

hostName = socket.gethostname()
server_IP = socket.gethostbyname(hostName) 
port = 50000

print("Hostname:",hostName, "IP:", server_IP) 

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

screenWidth = 800
screenHeight = 800
pygame.display.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))

tank = pygame.image.load('tankGreen.png')
tankSize = tank.get_width()
p1Tank = Tank(1, Rect(screenWidth-tankSize*2,(screenHeight-tankSize)/2,
            tankSize,tankSize), 270, 5)
p2Tank = Tank(2, Rect(tankSize,(screenHeight-tankSize)/2,tankSize,tankSize), 90, 5)
background=pygame.image.load('tankBackground.png')
background=pygame.transform.scale(background,(800,800))

running = True
playing = True
SINGLEPLAYER = True
headerSize = 10

tanks = {}
tanks[0] = tank
tankList = [p1Tank,p2Tank]
tankSpeed = 5

projectileSize = 10
projectiles = {}
projectilesLock = threading.Lock()

projectileSpeed = 1.0
reloadSpeed = 1
clock=pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)
textP1Lives = font.render(f'Player 1 Lives: {p1Tank.lives}', True, black, white)
textP2Lives = font.render(f'Player 2 Lives: {p2Tank.lives}', True, black, white)
textGameOver = font.render('Game Over', True, black, white)

tankRotationSpeed = 5
for i in range(tankRotationSpeed, 359, tankRotationSpeed):
    tanks[i] = rot_center(tank,-i)

if SINGLEPLAYER != True:
    server = input('Do you want to start the server?')
    if server.count('y'or'Y'):
        x.bind((hostName,port))
        print("Bound to address ",x.getsockname())
        x.listen(1)
        conn,addr = x.accept()
        thisUser = p1Tank
        pygame.display.set_caption('Player One')
    else:
        server_IP=input("Server IP:")
        x.connect((server_IP,port))
        conn = x
        thisUser = p2Tank
        pygame.display.set_caption('Player Two')
else:
    thisUser = p1Tank


clock = pygame.time.Clock()

def receive():
    global thisUser, projectiles, p1Tank, p2Tank, textP2Lives, textP1Lives, playing
    while running:
        msg_buffer = b''
        new_msg = True
        while True:

            if (new_msg and len(msg_buffer) < headerSize) \
                or (not new_msg and len(msg_buffer) < headerSize+msglen):
                msg = conn.recv(1024)
                msg_buffer += msg

            if new_msg:
                msglen = int(msg_buffer[:headerSize])
                new_msg = False

            if len(msg_buffer)-headerSize >= msglen: # full message
                decoded_msg = msg_buffer[headerSize:headerSize + msglen].decode()

                if decoded_msg.count('tank'):
                    x = decoded_msg.split(':')
                    playerNumber = int(x[1])
                    for tank in tankList:
                        if tank.player == playerNumber:
                            tank.rect.x = float(x[2])
                            tank.rect.y = float(x[3])

                if decoded_msg.count('rotate'):
                    x = decoded_msg.split(':')
                    playerNumber = int(x[1])
                    for tank in tankList:
                        if tank.player == playerNumber:
                            tank.angle = int(x[2])

                if decoded_msg.count('fireClient'):
                    x = decoded_msg.split(':')
                    projectile = Projectile(guid.nextId(),float(x[2]),float(x[3]),
                        Rect(float(x[4]),float(x[5]), int(x[6]),int(x[7])),int(x[8]))
                    projectilesLock.acquire()
                    projectiles[projectile.Id] = projectile
                    projectilesLock.release()
                    assert projectiles[projectile.Id].player != 1
                    msg = f'fireServer:{projectile.Id}:{projectile.xStep}:\
                        {projectile.yStep}:{projectile.rect.x}:{projectile.rect.y}:\
                        {projectile.rect.width}:{projectile.rect.height}:\
                        {projectile.player}'.encode()
                    msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                    conn.send(msg)

                if decoded_msg.count('fireServer'):
                    x = decoded_msg.split(':')
                    projectilesLock.acquire()
                    projectiles[x[1]]=Projectile(int(x[1]),float(x[2]),float(x[3]),
                        Rect(float(x[4]),float(x[5]), int(x[6]),int(x[7])),int(x[8]))
                    projectilesLock.release()

                if decoded_msg.count('projUpdate'):
                    assert thisUser.player != 1
                    x = decoded_msg.split(':')

                    projectilesLock.acquire()
                    for key, projectile in projectiles.items():
                        if projectile.Id == int(x[3]):
                            projectile.rect.x = float(x[1])
                            projectile.rect.y = float(x[2])
                    projectilesLock.release()
                if decoded_msg.count('livesUpdate'):
                    x=decoded_msg.split(':')
                    p1Tank.lives=x[1]
                    p2Tank.lives=x[2]
                    textP2Lives = \
                        font.render(f'Player 2 Lives: {p2Tank.lives}',
                        True, black, white)
                    textP1Lives = \
                        font.render(f'Player 1 Lives: {p1Tank.lives}',
                        True, black, white)
                if decoded_msg.count('projRemove'):
                    x=decoded_msg.split(':')
                    projectilesLock.acquire()
                    projectiles.pop(x[1])
                    projectilesLock.release()
                if decoded_msg.count('Gameover'):
                    playing=False

                new_msg = True
                msg_buffer = msg_buffer[headerSize+msglen:]

def eventLoop():
    global running, thisUser, otherUser, projectiles, projectile
    pygame.key.set_repeat(50, 28)
    while running:

        event = pygame.event.poll()

        if event.type == pygame.NOEVENT:
            time.sleep(0.002)

        elif event.type == pygame.QUIT:
            # TODO send quit to client
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                # TODO send quit to client
                running = False

            if playing: 
                # UP
                if event.key == pygame.K_w:
                    radians = math.radians(thisUser.angle)
                    thisUser.rect.x = min(max(0,thisUser.rect.x +
                        tankSpeed*math.sin(radians)),screenWidth -
                        thisUser.rect.width)
                    thisUser.rect.y = min(max(0+textP1Lives.get_height()/2,thisUser.rect.y -
                        tankSpeed*math.cos(radians)),screenHeight -
                        thisUser.rect.height)

                    if SINGLEPLAYER != True:
                        msg=f'tank:{thisUser.player}:{thisUser.rect.x}:\
                            {thisUser.rect.y}'.encode()
                        msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                        conn.send(msg)
                # DOWN
                if event.key == pygame.K_s: # down
                    radians = math.radians(thisUser.angle)
                    thisUser.rect.x = min(max(0,thisUser.rect.x -
                        tankSpeed*math.sin(radians)),screenWidth -
                        thisUser.rect.width)
                    thisUser.rect.y = min(max(0+textP1Lives.get_height()/2,thisUser.rect.y +
                        tankSpeed * math.cos(radians)),screenHeight -
                        thisUser.rect.height)
                    if SINGLEPLAYER != True:
                        msg=f'tank:{thisUser.player}:{thisUser.rect.x}:\
                            {thisUser.rect.y}'.encode()
                        msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                        conn.send(msg)
                # ROTATE CLOCKWISE
                if event.key == pygame.K_d:
                    thisUser.angle = (thisUser.angle + tankRotationSpeed) % 360
                    if SINGLEPLAYER != True:
                        msg=f'rotate:{thisUser.player}:{thisUser.angle}'.encode()
                        msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                        conn.send(msg)
                # ROTATE COUNTER-CLOCKWISE
                if event.key == pygame.K_a:
                    thisUser.angle = (thisUser.angle - tankRotationSpeed) % 360
                    if SINGLEPLAYER != True:
                        msg = f'rotate:{thisUser.player}:{thisUser.angle}'.encode()
                        msg = bytes(f"{len(msg):<{headerSize}}",'utf-8') + msg
                        conn.send(msg)
                # FIRE
                if event.key == pygame.K_SPACE:
                    currTime = time.time()
                    if thisUser.lastFired < currTime - reloadSpeed:
                        thisUser.lastFired = currTime
                        radians = math.radians(thisUser.angle)
                        x = thisUser.rect.x+(thisUser.rect.width-projectileSize)/2
                        y = thisUser.rect.y+(thisUser.rect.height-projectileSize)/2
                        projectile = Projectile(guid.nextId(),
                            projectileSpeed*math.sin(radians),
                            -projectileSpeed * math.cos(radians),
                            Rect(x, y, projectileSize, projectileSize),
                            thisUser.player)

                        if SINGLEPLAYER == True:
                            projectilesLock.acquire()
                            projectiles[projectile.Id] = projectile
                            projectilesLock.release()
                        else:
                            if thisUser.player==1:
                                projectilesLock.acquire()
                                projectiles[projectile.Id] = projectile
                                projectilesLock.release()
                                msg=f'fireServer:{projectile.Id}:{projectile.xStep}:\
                                    {projectile.yStep}:{projectile.rect.x}:\
                                    {projectile.rect.y}:{projectile.rect.width}:\
                                    {projectile.rect.height}:\
                                    {projectile.player}'.encode()
                                msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                                conn.send(msg)
                            else:
                                projectile.Id = -1
                                msg=f'fireClient:{projectile.Id}:{projectile.xStep}:\
                                {projectile.yStep}:{projectile.rect.x}:\
                                {projectile.rect.y}:{projectile.rect.width}:\
                                {projectile.rect.height}:{projectile.player}'.encode()
                                msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                                conn.send(msg)

def projectile():
    global projectiles
    global radians
    global textP1Lives, textP2Lives
    global playing

    assert thisUser.player == 1
    while running:
        if playing:
            keysToRmv = []
            projectilesLock.acquire()
            for key, projectile in projectiles.items():
                if projectile.rect.x >= screenWidth \
                    or projectile.rect.x+projectileSize <= 0 \
                    or projectile.rect.y+projectileSize <= textP1Lives.get_height() \
                    or projectile.rect.y >= screenHeight:

                    #REMOVE
                    keysToRmv.append(key)
                for tank in tankList:
                    if projectile.collideRect(tank,20):

                        #REMOVE
                        tank.reduceLife()
                        if SINGLEPLAYER!=True:
                            msg =f'livesUpdate:{p1Tank.lives}:{p2Tank.lives}'.encode()
                            msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                            conn.send(msg)
                        keysToRmv.append(key)
                        textP2Lives = \
                            font.render(f'Player 2 Lives: {p2Tank.lives}',
                            True, black, white)
                        textP1Lives = \
                            font.render(f'Player 1 Lives: {p1Tank.lives}',
                            True, black, white)

                        if p2Tank.lives == 0 or p1Tank.lives == 0:
                            playing = False
                            if SINGLEPLAYER != True:
                                msg =f'Gameover'.encode()
                                msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                                conn.send(msg)
                #UPDATE
                projectile.rect.x += projectile.xStep
                projectile.rect.y += projectile.yStep
                if SINGLEPLAYER!=True:
                    msg = f'projUpdate:{projectile.rect.x}:{projectile.rect.y}:\
                        {projectile.Id}'.encode()
                    msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                    conn.send(msg)

            for key in keysToRmv:
                projectiles.pop(key)
                if SINGLEPLAYER!=True:
                    msg =f'projRemove:{key}'.encode()
                    msg = bytes(f"{len(msg):<{headerSize}}",'utf-8')+msg
                    conn.send(msg)

            projectilesLock.release()

        time.sleep(0.002)


def render():
    screen.blit(background,(0,0,800,800))
    #screen.fill((220,190,150))
    screen.blit(tanks[p1Tank.angle],p1Tank.rect.toPygame())
    screen.blit(tanks[p2Tank.angle],p2Tank.rect.toPygame())

    if playing:
        projectilesLock.acquire()
        for key , proj in projectiles.items():
            pygame.draw.rect(screen,red,proj.rect.toPygame())
        projectilesLock.release()
    else:
        screen.blit(textGameOver,((screenWidth-textGameOver.get_width())//2,
            screenHeight//2))

    screen.blit(textP1Lives,(0,0))
    screen.blit(textP2Lives, (screenWidth-textP2Lives.get_width(),0))
    pygame.display.flip()

event_thread = threading.Thread(target=eventLoop)
event_thread.start()

if thisUser.player == 1:
    proj_thread = threading.Thread(target=projectile)
    proj_thread.start()

if SINGLEPLAYER != True:
    recv_thread = threading.Thread(target=receive)
    recv_thread.start()
fps=[]
while running:

    render()
    fps.append(clock.get_fps())
    clock.tick(60)
    if len(fps) == 60:
        print('mean:',round(statistics.mean(fps),2),'median:',round(statistics.median(fps),2),
            'min:',round(min(fps),2),'max:',round(max(fps),2))
        fps=[]

sys.exit()
pygame.quit()
