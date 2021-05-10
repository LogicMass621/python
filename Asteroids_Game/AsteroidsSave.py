#!/usr/bin/python
import pygame
import threading
import random
import time
import math
import sys
from utils import get_random_velocity, load_sprite, wrap_position
from pygame.math import Vector2

#changes name of terminal window
sys.stdout.write("\x1b]2;Asteroids!\x07")

#Set up the game window
pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)
weapon0Sound=pygame.mixer.Sound('assets/sounds/weapon0Sound.wav')
weapon0Sound.set_volume(0.0)
screenWidth, screenHeight = 640, 480

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Asteroids!')

#Control
projectiles = {}
projectilesLock = threading.Lock()

running = True
clock = pygame.time.Clock()



class Rect:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(int(self.__x), int(self.__y),
                                      self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(
            self.__x, self.__y, self.__width, self.__height)

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

    def colliderect(self, other, yAdjustment, xAdjustment):
        x = other.x + xAdjustment
        y = other.y + yAdjustment
        width = other.width - xAdjustment * 2
        height = other.height - yAdjustment * 2
        if self.x + self.width >= x and \
                x+width >= self.x and \
                self.y + self.height >= y and \
                y+height >= self.y:
            return True
        else:
            return False

    def rectintersection(self, other):
        x5 = max(self.x, other.x)
        x6 = min(self.x + self.width, other.x + other.width)
        y5 = max(self.y, other.y)
        y6 = min(self.y + self.height, other.y + other.height)
        if x5 >= x6 or y5 >= y6:
            return Rect(0, 0, 0, 0)
        return Rect(x5, y5, x6 - x5, y6 - y5)
      
    def toPygame(self):
        return self.__pyg_rect


#ASTEROIDS============================================


class Asteroid:
    def __init__(self, rect, image, xstep, ystep,uniqueId2,health,stage):
        self.__rect = rect
        self.__image = image
        self.__xstep = xstep
        self.__ystep = ystep
        self.__uniqueId2 = uniqueId2
        self.__health=health
        self.__stage=stage

    def __str__(self):
        return 'rect: {} xstep: {} ystep{}'.format(self.__rect, self.__xstep,
                                                   self.__ystep,self.__uniqueId2)

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    @property
    def xstep(self):
        return self.__xstep

    @property
    def ystep(self):
        return self.__ystep
    @property
    def uniqueId2(self):
        return self.__uniqueId2

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health
    @property
    def stage(self):
        return self.__stage

    @stage.setter
    def stage(self, stage):
        self.__stage = stage

class Projectile:
  def __init__(self, rect, xstep, ystep, Id,Type,Range,shotCoordx, shotCoordy,damage,explCounter,explX,explY,reloadTime):
      self.__rect = rect
      self.__xstep = xstep
      self.__ystep = ystep
      self.__Type = Type
      self.__Id = Id
      self.__Range = Range
      self.__shotCoordx=shotCoordx
      self.__shotCoordy=shotCoordy
      self.__damage=damage
      self.__explCounter = explCounter
      self.__explX = explX
      self.__explY = explY
      self.__time = time

      def __str__(self):
          return 'rect: {} xstep: {} ystep{}'.format(self.__rect,self.__xstep, self.__ystep)
          
      @property
      def rect(self):
          return self.__rect

      @rect.setter
      def rect(self, rect):
          self.__rect = rect

      @property
      def xstep(self):
          return self.__xstep

      @property
      def Type(self):
          return self.__Type

      @property
      def Id(self):
          return self.__Id

      @property
      def ystep(self):
          return self.__ystep
      @property
      def Range(self):
          return self.__Range
      @property
      def shotCoordx(self):
          return self.__shotCoordx
      @property
      def shotCoordy(self):
          return self.__shotCoordy
      @property
      def damage(self):
          return self.__damage
      @property
      def explCounter(self):
          return self.__explCounter

      @explCounter.setter
      def explCounter(self, explCounter):
          self.__explCounter = explCounter
      @property
      def explX(self):
          return self.__explX
      @property
      def explY(self):
          return self.__explY

      @property
      def reloadTime(self):
          return self.__reloadTime
      @reloadTime.setter
      def reloadTime(self, reloadTime):
          self.__reloadTime = reloadTime

Shiphealth = 1000

UP = Vector2(0, -1)

class Object:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Ship(Object):
  Control = 3
  Acceleration = 0.25

  def __init__(self, position):
    self.direction = Vector2(UP)

    super().__init__(position, load_sprite("ship"), Vector2(0))

  def rotate(self, clockwise=True):
    self.direction = Vector2(UP)
    sign = 1 if clockwise else -1
    angle = self.Control * sign
    self.direction.rotate_ip(angle)

  def accelerate(self):
    self.velocity += self.direction * self.Acceleration

  def draw(self, surface):
    angle = self.direction.angle_to(UP)
    rotated_surface = rotozoom(self.sprite, angle, 1.0)
    rotated_surface_size = Vector2(rotated_surface.get_size())
    blit_position = self.position - rotated_surface_size * 0.5
    surface.blit(rotated_surface, blit_position)

screenWidth, screenHeight = 640, 480
astList = {}
astImage = pygame.image.load('assets/images/asteroid.png')
uniqueId2=0
astLock=threading.Lock()

def asteroidThread():
    global running,projectiles
    while running:
        keysToRmv=[]
        astLock.acquire()
        for astKey,ast in astList.items():

            ast.rect.x += ast.xstep
            ast.rect.y += ast.ystep

            #check for boundaries and come in from other side
            if ast.rect.x > screenWidth:
                ast.rect.x = 0 - ast.rect.width

            if ast.rect.x + ast.rect.width < 0:
                ast.rect.x = screenWidth

            if ast.rect.y > screenHeight:
                ast.rect.y = 0 - ast.rect.height

            if ast.rect.y + ast.rect.height < 0:
                ast.rect.y = screenHeight

        astLock.release()

        time.sleep(0.07)


ast_thread = threading.Thread(target=asteroidThread)
ast_thread.start()

def createAsteroids(Number_of_asteroids):
  global uniqueId2
  #creating random asteroids
  for i in range(Number_of_asteroids):

      #temporary rect to create asteroid, to create asteroid
      w,h=random.randint(60, 80),random.randint(60,80)
      while abs(w-h) > 10:
          w,h=random.randint(60, 80),random.randint(60,80)

      astRect = Rect(random.randint(0, screenWidth),
                     random.randint(0, screenHeight), w,
                     h)

      #just to make sure asteroids move faster
      astSpeed=5
      Min,Max=-1,1
      xstep=round(random.uniform(Min,Max),2)*astSpeed
      ystep=round(random.uniform(Min,Max),2)*astSpeed
      while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
          xstep=round(random.uniform(Min,Max),2)*astSpeed
          ystep=round(random.uniform(Min,Max),2)*astSpeed


      #adding asteroid object to list
      image=pygame.transform.scale(astImage, (astRect.width+5, astRect.height+5))
      image=pygame.transform.flip(image,random.choice([True,False]),random.choice([True,False]))
      ast=(Asteroid(
              astRect,
              image,
              xstep, ystep,uniqueId2,((w*h)/30+20),1))
      print(ast.health,ast.stage)
          
      astLock.acquire()
      astList[uniqueId2]=ast
      astLock.release()
      uniqueId2+=1

def createAsteroid(x,y,w,h,xstep,ystep,astStage):
    global uniqueId2

    astRect = Rect(x,y,w,h)

    #adding asteroid object to list
    image=pygame.transform.scale(astImage, (astRect.width+5, astRect.height+5))
    image=pygame.transform.flip(image,random.choice([True,False]),random.choice([True,False]))
    ast=Asteroid(
            astRect,
            image,
            xstep*2, ystep*2,uniqueId2,((w*h)/30)+20,astStage)
    astLock.acquire()
    astList[uniqueId2] = ast
    astLock.release()

    uniqueId2+=1

#difficulty
AstNum=10
createAsteroids(AstNum)
#=====================================================

#Images
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

shipWidth=30
shipHeight=38
shipImage = pygame.transform.scale(pygame.image.load("assets/images/ship.png"),(shipWidth,shipHeight))
shipRotation = 5
ships = {}
ships[0] = shipImage

for i in range(shipRotation, 359, shipRotation):
  ships[i] = rot_center(shipImage, -i)

shipX = (screenWidth / 2) - (shipWidth / 2)
shipY = (screenHeight / 2) - (shipHeight / 2)
shipRect = Rect(shipX, shipY, shipWidth, shipHeight)
ship = Ship(0)
ship.rect=shipRect
ship.angle=0
ship.health=1000
SVel=0
BVel=0
FVel=0

shipCoords={}
shipCoords[0]=(ships[0].get_rect().x-ships[0].get_rect().width/2+ship.rect.x,ships[0].get_rect().y-ships[0].get_rect().height/2+ship.rect.y)
for i in range(shipRotation,359,shipRotation):
  shipCoords[i]= (ships[i].get_rect().x-ships[i].get_rect().width/2+ship.rect.x,ships[i].get_rect().y-ships[i].get_rect().height/2+ship.rect.y)

w0explosion = pygame.image.load('assets/images/weapon0explosion.png')
w0explosion=pygame.transform.scale(w0explosion,(20,20))


#Each weapon will have it's own number/state
currentWeapon = 0
weaponPrevTimes = {}
weaponPrevTimes[currentWeapon]=0
uniqueId=0

def eventLoop():
    SVel=0
    BVel=0
    FVel=0
    global projectiles, currentWeapon, uniqueId, weaponPrevTimes, Svel, Bvel, Fvel
    pygame.key.set_repeat(50,50)
    while running:
        pygame.display.init()
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            #Shoot (Code Collapsed)
            if event.key == pygame.K_SPACE:

                if currentWeapon == 0:
                  Reload=.25
                  Range=125
                  projectileSize = 3
                  damage=30
                  currTime=time.time()

                  if currTime-weaponPrevTimes[currentWeapon]>=Reload:

                    weapon0Sound.stop()
                    weapon0Sound.play()
                    roundedAngle=((5 * round(ship.angle/5))%360)
                    x = shipCoords[roundedAngle][0]
                    y = shipCoords[roundedAngle][1]
                    projectileRect = Rect(x+ships[roundedAngle].get_rect().width/2,
                      y+ships[roundedAngle].get_rect().height/2,
                       projectileSize, projectileSize)
                    radians = math.radians(ship.angle)
                    projectileSpeed = 0.0015
                    projectileType = 0
                    uniqueId += 1
                    proj=Projectile(
                        projectileRect, 0,
                        0, 0,
                        uniqueId,0,0,0,0,0,0,0,0)

                    #have to like redefine attributes for some reason
                    minSpray,maxSpray=(-.3,.3)
                    proj.rect=projectileRect
                    proj.xstep=projectileSpeed * math.sin(radians+random.uniform(minSpray,maxSpray))
                    proj.ystep=-projectileSpeed * math.cos(radians+random.uniform(minSpray,maxSpray))
                    proj.Type=0
                    proj.explCounter=0
                    proj.Range=Range
                    proj.shotCoordx=proj.rect.x
                    proj.shotCoordy=proj.rect.y
                    proj.damage=damage
                    proj.explX=0
                    proj.explY=0
                    proj.reloadTime=time.time()
                    projectilesLock.acquire()
                    projectiles[uniqueId]=proj
                    projectilesLock.release()
                    weaponPrevTimes[currentWeapon]=time.time()

            #Forward
            is_key_pressed = pygame.key.get_pressed()

            if is_key_pressed[pygame.K_RIGHT]:
              print("right")
              ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
              print("left")
              ship.rotate(clockwise=False)
    #print(ship.Svel)
    ship.angle=(SVel+5)%360
    ship.angle = (ship.angle / 2)
    time.sleep(0.08)

#can't just pass rect becuase ship might move, and range calculations would be off
def dist_to(x1,y1,width1,height1,rect):
  dist=math.sqrt((x1+width1/2-rect.x+rect.width/2)
    *(x1+width1/2-rect.x+rect.width/2)
    +(y1+height1/2-rect.y+rect.height/2)*(y1+height1/2-rect.y+rect.height/2))
  
  return dist
    
event_thread = threading.Thread(target=eventLoop)
event_thread.start()
projExplosions=[]
points=0
white=(255,255,255)
textPoints = font.render(f'Points: {points}', True, white, None)


def proj_thread():
  global projectiles,running,asteroids,projExplosions,AstNum,points,textPoints
  while running:

    keysToRmv=[]
    astToRmv=[]
    astCreate=[]

    projectilesLock.acquire()
    for projKey, proj in projectiles.items():
      if proj.Type==0:
        currTime=time.time()
        timePast=(currTime-proj.reloadTime)*100000
        if timePast>20:
          proj.rect.x += timePast*proj.xstep
          proj.rect.y += timePast*proj.ystep
          proj.reloadTime=time.time()

      if dist_to(proj.shotCoordx,proj.shotCoordy,proj.rect.width,proj.rect.height,proj.rect)>=proj.Range:
        keysToRmv.append(projKey)
      astLock.acquire()
      for astKey,ast in astList.items():
        if ast.rect.colliderect(proj.rect,(ast.image.get_rect().width-ast.rect.width),(ast.image.get_rect().height-ast.rect.height)):
          currTime=time.time()
          if proj.Type==0:
            proj.explX=proj.rect.x-10
            proj.explY=proj.rect.y-10  # 10 is half width of explosion, no variable, only used here

          projExplosions.append(proj)
          ast.health -= proj.damage
          keysToRmv.append(projKey)
          if ast.health<=0:
            stage=ast.stage
            points+=(stage*50)
            textPoints = font.render(f'Points: {points}', True, white, None)
            astToRmv.append(astKey)
            if ast.rect.width>=20 and ast.rect.height>=20:

              var5=random.randint(-5,5)
              var6=random.randint(-5,5)
              area=(ast.rect.width*ast.rect.height)/2
              width1=int(math.sqrt(area)+var5)
              height1=int(math.sqrt(area)-var5)
              width2=int(math.sqrt(area)+var6)
              height2=int(math.sqrt(area)-var6)
              popDistance=(ast.rect.width+ast.rect.height)/6
              astSpeed=6
              Min,Max=0.5,0.9

              xstep=round(random.uniform(Min,Max),2)*astSpeed
              ystep=round(random.uniform(Min,Max),2)*astSpeed
              while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
                xstep=round(random.uniform(Min,Max),2)*astSpeed
                ystep=round(random.uniform(Min,Max),2)*astSpeed

              xstep2=round(random.uniform(Min,Max),2)*astSpeed
              ystep2=round(random.uniform(Min,Max),2)*astSpeed
              while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
                xstep2=round(random.uniform(Min,Max),2)*astSpeed
                ystep2=round(random.uniform(Min,Max),2)*astSpeed

              var1=random.choice([1,-1])
              var2=random.choice([1,-1])
              var3=random.choice([1,-1])
              var4=random.choice([1,-1])

              x=ast.rect.x+ast.rect.width/2-width1/2+popDistance*var1
              y=ast.rect.y+ast.rect.height/2-height1/2+popDistance*var2

              x2=ast.rect.x+ast.rect.width/2-width2/2+popDistance*var3
              y2=ast.rect.y+ast.rect.height/2-height2/2+popDistance*var4

              astCreate.append((x,y,width1,height1,xstep*var1,ystep*var2,(stage+1)))

              astCreate.append((x2,y2,width2,height2,xstep2*var3,ystep2*var4,(stage+1)))


      astLock.release()


    for key in keysToRmv:
      if key in projectiles:
        projectiles.pop(key)
    projectilesLock.release()

    for i in range(len(astCreate)):
      createAsteroid(*astCreate[i])
    astLock.acquire()

    for key in astToRmv:
      astList.pop(key)
    astLock.release()
    if len(astList)<AstNum*4/5:
        print('if')

        w,h=random.randint(60, 80),random.randint(60, 80)
        while abs(w-h) > 22:
          print('while')
          w,h=random.randint(60, 80),random.randint(60, 80)
        choose=random.randint(0,1)
        astSpeed=5
        Min,Max=-1,1

        if choose == 0:
          print('x')
          xpos=random.randint(0,1)
          if xpos==0:
            print('x:0')
            x=0-w
            xstep=round(random.uniform(0,1),2)*astSpeed
            ystep=round(random.uniform(Min,Max),2)*astSpeed
            while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
              xstep=round(random.uniform(0,1),2)*astSpeed
              ystep=round(random.uniform(Min,Max),2)*astSpeed
          if xpos==1:
            print('x:1')
            x=screenWidth
            xstep=round(random.uniform(-1,0),2)*astSpeed
            ystep=round(random.uniform(Min,Max),2)*astSpeed
            while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
              xstep=round(random.uniform(-1,0),2)*astSpeed
              ystep=round(random.uniform(Min,Max),2)*astSpeed
          y=random.randint(0,screenHeight)
        if choose == 1:
          print('y')
          ypos=random.randint(0,1)
          if ypos==0:
            print('y:0')
            y=0-h
            ystep=round(random.uniform(0,1),2)*astSpeed
            xstep=round(random.uniform(Min,Max),2)*astSpeed
            while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
              ystep=round(random.uniform(0,1),2)*astSpeed
              xstep=round(random.uniform(Min,Max),2)*astSpeed
          if ypos==1:
            print('y:1')
            y=screenHeight
            ystep=round(random.uniform(-1,0),2)*astSpeed
            xstep=round(random.uniform(Min,Max),2)*astSpeed
            while math.sqrt(xstep*xstep+ystep*ystep)<1.5:
              ystep=round(random.uniform(-1,0),2)*astSpeed
              xstep=round(random.uniform(Min,Max),2)*astSpeed
          x=random.randint(0,screenHeight)
          createAsteroid(x,y,w,h,xstep,ystep)

      
  time.sleep(0.08)


proj_thread = threading.Thread(target=proj_thread)
proj_thread.start()
#Functions
#=====================================================


w0color= (175, 155, 96)

#Updating
def render():
  global projectiles,projExplosions
  screen.fill(0)

  screen.blit(textPoints,(0,0))

  #asteroids
  for key,ast in astList.items():
      screen.blit(ast.image, ast.rect.toPygame())

  #projectiles
  projectilesLock.acquire()
  for key, proj in projectiles.items():
    if proj.Type==0:
      pygame.draw.rect(screen, w0color, proj.rect.toPygame())
  projectilesLock.release()

  #explosions
  for proj in projExplosions:
    if proj.Type==0:
      screen.blit(w0explosion, (proj.explX,proj.explY))
      proj.explCounter+=1
      if proj.explCounter==4:
        projExplosions.remove(proj)

  #ship
  roundedAngle=((5 * round(ship.angle/5))%360)
  screen.blit(ships[roundedAngle], shipCoords[roundedAngle])

  pygame.display.flip()


while running:
    render()
    clock.tick(60)
pygame.quit()
exit(0)