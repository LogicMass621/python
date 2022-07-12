#!/usr/bin/python
import pygame
import threading
import random
import time
import math
import sys

#changes name of terminal window
sys.stdout.write("\x1b]2;Rocks!\x07")

#Set up the game window
pygame.mixer.pre_init(44100, -16, 1, 512)   #fixes sound delay
pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)
weapon0Sound=pygame.mixer.Sound('assets/sounds/weapon0Sound.wav')
weapon0Sound.set_volume(0.05)
screenWidth, screenHeight = 640, 480
spaceImage=pygame.image.load('assets/images/space.png')

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Rocks!')

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

    #def __str__(self):
        #return 'rect: {} xstep: {} ystep{}'.format(self.__rect, self.__xstep,
                                                   #self.__ystep,self.__uniqueId2)

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
  def __init__(self, rect, xstep, ystep, Id,Type,Range,shotCoordx, shotCoordy,damage,explCounter,explX,explY, reloadTime):
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
    self.__reloadTime = reloadTime

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
  @shotCoordy.setter
  def shotCoordy(self, shotCoordy):
      self.__shotCoordy = shotCoordy
  @shotCoordx.setter
  def shotCoordx(self, shotCoordx):
      self.__shotCoordx = shotCoordx
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
  @explX.setter
  def explX(self, explX):
      self.__explX = explX
  @explY.setter
  def explY(self, explY):
      self.__explY = explY
  @property
  def reloadTime(self):
      return self.__reloadTime

  @reloadTime.setter
  def reloadTime(self, reloadTime):
      self.__reloadTime = reloadTime

class Ship:
  def __init__(self,rect,angle,health,xVel,yVel,rotSpeed):
    self.__rect = rect
    self.__angle = angle
    self.__health = health
    self.__xVel = xVel
    self.__yVel = yVel
    self.__rotSpeed = rotSpeed

  @property
  def rect(self):
      return self.__rect

  @rect.setter
  def rect(self, rect):
      self.__rect = rect

  @property
  def angle(self):
      return self.__angle

  @angle.setter
  def angle(self, angle):
      self.__angle = angle

  @property
  def health(self):
      return self.__health

  @health.setter
  def health(self, health):
      self.__health = health

  @property
  def xVel(self):
      return self.__xVel

  @xVel.setter
  def xVel(self, xVel):
      self.__xVel = xVel

  @property
  def yVel(self):
      return self.__yVel

  @yVel.setter
  def yVel(self, yVel):
      self.__yVel = yVel

  @property
  def rotSpeed(self):
      return self.__rotSpeed

  @rotSpeed.setter
  def rotSpeed(self, rotSpeed):
      self.__rotSpeed = rotSpeed
 

#Images
def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

shipWidth=30
shipHeight=38
shipIcon = pygame.image.load("assets/images/shipIcon.png")
shipImage = pygame.transform.scale(pygame.image.load("assets/images/ship.png"),(shipWidth,shipHeight))
invulnShipImage=pygame.transform.scale(pygame.image.load("assets/images/invulnShip.png"),(shipWidth,shipHeight))
shipRotation = 5
ships = {}
invulnShips={}
invulnShips[0]=invulnShipImage
ships[0] = shipImage
invulnLength=3
invulnDrawTimer=time.time()


for i in range(shipRotation, 719, shipRotation):
  ships[i/2] = rot_center(shipImage, -i/2)
for i in range(shipRotation, 719, shipRotation):
  invulnShips[i/2] = rot_center(invulnShipImage, -i/2)

shipX = (screenWidth / 2) - (shipWidth / 2)
shipY = (screenHeight / 2) - (shipHeight / 2)
shipRect = Rect(shipX, shipY, shipWidth, shipHeight)
playerShip = Ship(0,0,0,0,0,0)
playerShip.rect=shipRect
playerShip.rotSpeed=0
playerShip.health=5
playerShip.xVel=0
playerShip.yVel=0
playerShip.angle=0
textColor= (255,107,0)      

screenWidth, screenHeight = 640, 480
astList = {}
astImage = pygame.image.load('assets/images/asteroid.png')
tempAstImage = pygame.image.load('assets/images/tempAst.png')
uniqueId2=0

astTimer=time.time()
astPrevTimes={}

#difficulty
AstNum=4

for i in range(AstNum):
  astPrevTimes[i]=time.time()
homeScreen=True

def dist_to(x1,y1,width1,height1,rect):
  dist=math.sqrt((x1+width1/2-rect.x+rect.width/2)
    *(x1+width1/2-rect.x+rect.width/2)
    +(y1+height1/2-rect.y+rect.height/2)*(y1+height1/2-rect.y+rect.height/2))
  
  return dist
  
astLock=threading.Lock()

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
      while dist_to(astRect.x,astRect.y,astRect.width,astRect.height,shipRect)<200:

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
          
      astLock.acquire()
      astList[uniqueId2]=ast
      astLock.release()
      uniqueId2+=1

def createAsteroid(x,y,w,h,xstep,ystep,astStage):
    global uniqueId2,astPrevTimes

    astRect = Rect(x,y,w,h)

    #adding asteroid object to list
    image=pygame.transform.scale(astImage, (astRect.width+5, astRect.height+5))
    image=pygame.transform.flip(image,random.choice([True,False]),random.choice([True,False]))
    ast=Asteroid(
            astRect,
            image,
            xstep*2, ystep*2,uniqueId2,((w*h)/30)+20,astStage)
    astPrevTimes[uniqueId2]=time.time()
    astLock.acquire()
    astList[uniqueId2] = ast
    astLock.release()

    uniqueId2+=1

def splitAsteroid(ast):
  if ast.stage < 3 and homeScreen == False:
    var5=random.randint(-5,5)
    var6=random.randint(-5,5)
    area=(ast.rect.width*ast.rect.height)/2
    width1=int(math.sqrt(area)+var5)
    height1=int(math.sqrt(area)-var5)
    width2=int(math.sqrt(area)+var6)
    height2=int(math.sqrt(area)-var6)
    popDistance=(ast.rect.width+ast.rect.height)/18
    astSpeed=5
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
    while var1==var3 and var2==var4:
      var4=random.choice([1,-1])


    x=ast.rect.x+ast.rect.width/2-width1/2+popDistance*var1
    y=ast.rect.y+ast.rect.height/2-height1/2+popDistance*var2

    x2=ast.rect.x+ast.rect.width/2-width2/2+popDistance*var3
    y2=ast.rect.y+ast.rect.height/2-height2/2+popDistance*var4
    createAsteroid(x,y,width1,height1,xstep*var1,ystep*var2,(ast.stage+1))
    createAsteroid(x2,y2,width2,height2,xstep2*var3,ystep2*var4,(ast.stage+1))

createAsteroids(AstNum)

white=(255,255,255)

highestScore=0
highestScoreText=font.render(f'Highest Score: {highestScore}',True,white,None)
invulnTime=time.time()
tempAsts={}
tempAstRmv=[]
def asteroidThread():
    global running,projectiles,tempAstRmv, astTimer,astPrevTimes,homeScreen,invulnTime,points,invulnDrawTimer,points,textPoints
    while running:
      if homeScreen==False:
        roundedAngle=(2.5*round(playerShip.angle/2.5))%360
        keysToRmv=[]
        splitAst=[]
        shipRect=Rect(playerShip.rect.x-ships[roundedAngle].get_width()/2,playerShip.rect.y-ships[roundedAngle].get_height()/2, shipWidth,shipHeight)
        astLock.acquire()
        for astKey,ast in astList.items():
            astTimer=time.time()
            astDeltaTime=astTimer-astPrevTimes[astKey]

            ast.rect.x += ast.xstep*astDeltaTime*10
            ast.rect.y += ast.ystep*astDeltaTime*10
            roundedAngle=(2.5*round(playerShip.angle/2.5))%360
            shipRect=Rect(playerShip.rect.x-ships[roundedAngle].get_width()/2,playerShip.rect.y-ships[roundedAngle].get_height()/2,ships[roundedAngle].get_width(),ships[roundedAngle].get_height())
            if ast.rect.colliderect(shipRect,5,5) and time.time()-invulnTime>invulnLength:
              invulnDrawTimer=time.time()
              playerShip.health -=1
              points+=ast.stage*50
              textPoints = font.render(f'Points: {points}', True, textColor, None)
              invulnTime=time.time()
              shipRect = Rect(shipX, shipY, shipWidth, shipHeight)
              playerShip.rect=shipRect
              playerShip.rotSpeed=0
              playerShip.xVel=0
              playerShip.yVel=0
              playerShip.angle=0
              keysToRmv.append(astKey)
              splitAst.append(ast)

            if ast.rect.colliderect(shipRect,5,5) and time.time()-invulnTime<invulnLength:
              invulnTime=time.time()

            astPrevTimes[astKey]=time.time()

            #check for boundaries and come in from other side
            if ast.rect.x > screenWidth-ast.rect.width and ast.xstep>0:
              if not(ast.uniqueId2 in tempAsts.keys()):
                tempX=ast.rect.x
                ast.rect.x = 0 - ast.rect.width
                tempAstObj= Asteroid(Rect(tempX,ast.rect.y,ast.rect.width,ast.rect.height)
                  , ast.image, ast.xstep, ast.ystep,ast.uniqueId2,ast.health,ast.stage)
                tempAsts[tempAstObj.uniqueId2]=tempAstObj

            if ast.rect.x < 0 and ast.xstep<0:
              if not(ast.uniqueId2 in tempAsts.keys()):
                tempX=ast.rect.x
                ast.rect.x = screenWidth+ast.rect.x
                tempAstObj= Asteroid(Rect(tempX,ast.rect.y,ast.rect.width,ast.rect.height)
                  , ast.image, ast.xstep, ast.ystep,ast.uniqueId2,ast.health,ast.stage)
                tempAsts[tempAstObj.uniqueId2]=tempAstObj

            if ast.rect.y > screenHeight - ast.rect.height and ast.ystep>0:
              if not(ast.uniqueId2 in tempAsts.keys()):
                tempY=ast.rect.y
                ast.rect.y = 0-ast.rect.height
                tempAstObj= Asteroid(Rect(ast.rect.x,tempY,ast.rect.width,ast.rect.height)
                  , ast.image, ast.xstep, ast.ystep,ast.uniqueId2,ast.health,ast.stage)
                tempAsts[tempAstObj.uniqueId2]=tempAstObj

            if ast.rect.y < 0 and ast.ystep<0:
              if not(ast.uniqueId2 in tempAsts.keys()):
                tempY=ast.rect.y
                ast.rect.y = screenHeight+ast.rect.y
                tempAstObj= Asteroid(Rect(ast.rect.x,tempY,ast.rect.width,ast.rect.height)
                  , ast.image, ast.xstep, ast.ystep,ast.uniqueId2,ast.health,ast.stage)
                tempAsts[tempAstObj.uniqueId2]=tempAstObj

        for key,ast in tempAsts.items():
          if ast.rect.colliderect(shipRect,5,5) and time.time()-invulnTime>invulnLength:
              invulnDrawTimer=time.time()
              playerShip.health -=round(250*1/ast.stage) 
              points+=ast.stage*50
              textPoints = font.render(f'Points: {points}', True, textColor, None)
              invulnTime=time.time()
              shipRect = Rect(shipX, shipY, shipWidth, shipHeight)
              playerShip.rect=shipRect
              playerShip.rotSpeed=0
              playerShip.xVel=0
              playerShip.yVel=0
              playerShip.angle=0
              keysToRmv.append(ast.uniqueId2)
              splitAst.append(ast)
          ast.rect.x+=ast.xstep * astDeltaTime * 10
          ast.rect.y+=ast.ystep * astDeltaTime * 10
          astWidth=ast.image.get_width()
          astHeight= ast.image.get_height()
          if not(ast.rect.x+ast.rect.width >= 0 and \
            screenWidth >= ast.rect.x and \
            ast.rect.y+ast.rect.height >= 0 and \
            0+screenHeight >= ast.rect.y):
            tempAstRmv.append(ast.uniqueId2)
        for key in tempAstRmv:
          if key in tempAsts:
            tempAsts.pop(key)
        tempAstRmv=[]

        for key in keysToRmv:
          if key in tempAsts:
            tempAsts.pop(key)
          astList.pop(key)
        astLock.release()
        if playerShip.health<=0:
          homeScreen=True
          home_screen()
        for i in splitAst:
          splitAsteroid(i)
        time.sleep(0.08)


ast_thread = threading.Thread(target=asteroidThread)
ast_thread.start()


#=====================================================

def home_screen():
  global homeScreen, astList, projectiles,points,astPrevTimes,uniqueId,uniqueId2,textPoints,highestScore,highestScoreText,hyperCharge
  astLock.acquire()
  projectilesLock.acquire()
  uniqueId2=0
  uniqueId=0
  for i in range(AstNum):
    astPrevTimes[i]=time.time()
  homeScreen=True
  astList={}
  projectiles={}
  shipX = (screenWidth / 2) - (shipWidth / 2)
  shipY = (screenHeight / 2) - (shipHeight / 2)
  shipRect = Rect(shipX, shipY, shipWidth, shipHeight)
  playerShip.rect=shipRect
  playerShip.rotSpeed=0
  playerShip.health=1000
  playerShip.xVel=0
  playerShip.yVel=0
  playerShip.angle=0
  if points>highestScore:
    highestScore=points
    highestScoreText=font.render(f'Highest Score: {highestScore}',True,white,None)
  points=0
  textPoints = font.render(f'Points: {points}', True, textColor, None)
  hyperCharge=60
  currentWeapon = 0
  tempAsts={}
  astLock.release()
  projectilesLock.release()
  createAsteroids(AstNum)

w0explosion = pygame.image.load('assets/images/weapon0explosion.png')
w0explosion=pygame.transform.scale(w0explosion,(20,20))


#Each weapon will have it's own number/state
currentWeapon = 0
weaponPrevTimes = {}
weaponPrevTimes[currentWeapon]=0
uniqueId=0
prevTime=time.time()
is_key_pressed = pygame.key.get_pressed()

pygame.mixer.set_num_channels(8)
thrusterChannel=pygame.mixer.Channel(5)
thrusterAccelSound=pygame.mixer.Sound('assets/sounds/thrusterSound.wav')
thrusterAccelSound.set_volume(0.1)
maxSpeed=0.002
minSpeed=0.00004
hyperChargeLength=60
hyperCharge=hyperChargeLength
currTime=time.time()
prevTime=currTime
timePast=currTime-prevTime
#hyperChargeTime is the seconds it takes to fully charge bar
hyperChargeTime=7
def eventLoop():
    global projectiles, currentWeapon,invulnTime, uniqueId, weaponPrevTimes, homeScreen,running,prevTime,is_key_pressed,hyperCharge,timePast
    pygame.key.set_repeat(50,50)
    pygame.display.init()
    keyCheck=0.01
    fluidFriction=0.999995
    while running:
      if homeScreen==True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
          running=False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
          mouseRect=Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)
          if mouseRect.colliderect(buttonRect,0,0):
            homeScreen=False
            invulnTime=time.time()
      if homeScreen==False:
          event = pygame.event.poll()
          if event.type == pygame.QUIT:
            running=False
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:
                homeScreen=True
                home_screen()

          currTime=time.time()
          if currTime-prevTime>keyCheck:
              is_key_pressed = pygame.key.get_pressed()
              #Shoot (Code Collapsed)
              if is_key_pressed[pygame.K_SPACE]:

                  if currentWeapon == 0:
                    Reload=.25
                    Range=250
                    projectileSize = 3
                    damage=30
                    currTime=time.time()
                    minSpray,maxSpray=(0,0)
                    projectileSpeed = 0.002
                    recoil=1250
                    if currTime-weaponPrevTimes[currentWeapon]>=Reload and time.time()-invulnTime>invulnLength:

                      weapon0Sound.stop()
                      weapon0Sound.play()
                      radians = math.radians(playerShip.angle)
                      roundedAngle= roundedAngle=(2.5*round(playerShip.angle/2.5))%360
                      projectileRect = Rect(ships[roundedAngle].get_rect().x+playerShip.rect.x+math.sin(radians)*shipWidth,ships[roundedAngle].get_rect().y+playerShip.rect.y-math.cos(radians)*shipHeight,
                         projectileSize, projectileSize)
                      uniqueId += 1
                      proj=Projectile(
                          projectileRect, playerShip.xVel + projectileSpeed * math.sin(radians+random.uniform(minSpray,maxSpray)),
                          playerShip.yVel-projectileSpeed * math.cos(radians+random.uniform(minSpray,maxSpray)), uniqueId,
                          0,Range,0,0,damage,0,0,0,time.time())
                      playerShip.rect.x-=proj.xstep*recoil 
                      playerShip.rect.y-=proj.ystep*recoil
                      projectilesLock.acquire()
                      projectiles[uniqueId]=proj
                      projectilesLock.release()
                      weaponPrevTimes[currentWeapon]=time.time()
              timePast=currTime-prevTime
              if is_key_pressed[pygame.K_d]:
                playerShip.angle+=2.5

              if is_key_pressed[pygame.K_a]:
                playerShip.angle-=2.5
              if is_key_pressed[pygame.K_s] and math.floor(hyperCharge)==hyperChargeLength:
                playerShip.rect.x=random.randint(0,screenWidth)
                playerShip.rect.y=random.randint(0,screenHeight)
                hyperCharge=0
              if hyperCharge<hyperChargeLength:
                hyperCharge+=timePast*hyperChargeLength/hyperChargeTime #hyperChargeTime is the seconds it takes to fully charge bar
              else:
                pass

              if thrusterChannel.get_busy() == False and is_key_pressed[pygame.K_w]:
                thrusterChannel.play(thrusterAccelSound)
              if is_key_pressed[pygame.K_w] == False:
                thrusterAccelSound.stop()
              if is_key_pressed[pygame.K_w] and math.sqrt((playerShip.xVel*playerShip.xVel)+(playerShip.yVel*playerShip.yVel))<maxSpeed:
                radians = math.radians(playerShip.angle)
                playerShip.xVel += math.sin(radians)*timePast*0.0025
                playerShip.yVel += -math.cos(radians)*timePast*0.0025
              prevTime=currTime
          if playerShip.rect.x > screenWidth:
              playerShip.rect.x = 0 - playerShip.rect.width

          if playerShip.rect.x + playerShip.rect.width < 0:
              playerShip.rect.x = screenWidth

          if playerShip.rect.y > screenHeight:
              playerShip.rect.y = 0 - playerShip.rect.height

          if playerShip.rect.y + playerShip.rect.height < 0:
              playerShip.rect.y = screenHeight

      deltaFriction = math.pow(fluidFriction,timePast)
      playerShip.xVel=playerShip.xVel*fluidFriction
      playerShip.yVel=playerShip.yVel*fluidFriction
      playerShip.rect.x += playerShip.xVel
      playerShip.rect.y += playerShip.yVel


    time.sleep(0.08)
    
event_thread = threading.Thread(target=eventLoop)
event_thread.start()
projExplosions=[]
points=0
textPoints = font.render(f'Points: {points}', True, textColor, None)

def proj_thread():
  global projectiles,running,asteroids,projExplosions,AstNum,points,textPoints,astPrevTimes,homeScreen,invulnDrawTimer,AstNum, invulnTime,astList,astPrevTimes
  while running:
    while homeScreen==False:

      keysToRmv=[]
      astToRmv=[]
      splitAst=[]

      projectilesLock.acquire()
      for projKey, proj in projectiles.items():
        if proj.Type==0:
          currTime=time.time()
          timePast=(currTime-proj.reloadTime)*10
          if timePast>0.03:
            xChange=timePast*proj.xstep*10000
            yChange=timePast*proj.ystep*10000
            proj.rect.x += xChange
            proj.rect.y += yChange
            proj.shotCoordx+=xChange
            proj.shotCoordy+=yChange
            if proj.rect.x > screenWidth:
              proj.rect.x = 0

            if proj.rect.x < 0:
                proj.rect.x = screenWidth

            if proj.rect.y > screenHeight:
                proj.rect.y = 0
            if proj.rect.y < 0:
                proj.rect.y = screenHeight
            proj.reloadTime=time.time()

        if math.sqrt((proj.shotCoordx*proj.shotCoordx)+(proj.shotCoordy*proj.shotCoordy))>=proj.Range:
          keysToRmv.append(projKey)
        astLock.acquire()
        if len(tempAsts)>0:
          tempDict={}
          for key,ast in astList.items():
            tempDict[key]=ast
          for key,ast in tempAsts.items():
            tempDict[key+len(astList)]=ast
        else:
          tempDict=astList
        for astKey,ast in tempDict.items():
          if ast.rect.colliderect(proj.rect,5,5): #5 is ast.image.get_rect().width-ast.rect.width
            if proj.Type==0:
              proj.explX=proj.rect.x-10
              proj.explY=proj.rect.y-10  # 10 is half width of explosion, no variable, only used here

            projExplosions.append(proj)
            ast.health -= proj.damage
            keysToRmv.append(projKey)
            if ast.health<=0:
              stage=ast.stage
              points+=(stage*25)
              textPoints = font.render(f'Points: {points}', True, textColor, None)
              astToRmv.append(astKey)        
              splitAst.append(ast)        
        astLock.release()

      for key in keysToRmv:
        if key in projectiles:
          projectiles.pop(key)
      projectilesLock.release()

      for key in astToRmv:
        if key in astList:
          astLock.acquire()
          astList.pop(key)
          astLock.release()
        if key in tempAsts:
          tempAsts.pop(key)
      for i in splitAst:
        splitAsteroid(i)

      if len(astList)==0 and homeScreen == False:
        AstNum+=1
        createAsteroids(astNum)
        for astKey,ast in astList.items():
          astPrevTimes[astKey]=time.time()
        invulnTime=time.time()
        invulnDrawTimer=time.time()
      time.sleep(0.02)


proj_thread = threading.Thread(target=proj_thread)
proj_thread.start()
#Functions
#=====================================================


w0color=(255,121,26)
#(204, 255, 102)
black=(0,0,0)
playButton=font.render('PLAY',True,white,None)
buttonRect=Rect(screenWidth/2-playButton.get_width()/2, screenHeight/2-playButton.get_height()/2,playButton.get_width(),playButton.get_height())
bigFont = pygame.font.Font('freesansbold.ttf', 40)
asteroidsTitle=bigFont.render('Rocks!',True,white,None)
titleCoords=(screenWidth/2-asteroidsTitle.get_width()/2,screenHeight/2-asteroidsTitle.get_height()/2-playButton.get_height()*2)
hyperSpaceCoolBar=pygame.Surface((40,80))
hyperColor=(204,85,0,0.5)
hyperSpaceCoolBar.fill(hyperColor)
hyperSpaceCoolBar.set_alpha(128)

#Updating
def render():
  global projectiles,projExplosions,hyperCharge
  screen.blit(spaceImage,(0,0))
  if homeScreen==True:
    screen.blit(playButton,(buttonRect.x,buttonRect.y))
    screen.blit(asteroidsTitle,titleCoords)
    screen.blit(highestScoreText,(screenWidth/2-highestScoreText.get_width()/2,buttonRect.y+playButton.get_height()*3/2))
  if homeScreen==False:

    screen.blit(textPoints,(0,0))
    for i in range(playerShip.health):
      screen.blit(shipIcon,Rect(screenWidth-(i+1)*30,0,30,38).toPygame());
    #asteroids
    keyList={}
    astLock.acquire()
    for key,ast in astList.items():
        keyList[ast.uniqueId2]=[ast]
    for key,ast in tempAsts.items():
        if ast.uniqueId2 in keyList:
          keyList[ast.uniqueId2].append(ast)
        else:
          keyList[ast.uniqueId2]=[ast]
    astLock.release()
    for key, List in keyList.items():     #keeps draw order for temp asts
      for i in List:
        screen.blit(i.image, i.rect.toPygame())

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
        if proj.explCounter>=4:
          projExplosions.remove(proj)

    #ship
    roundedAngle=(2.5*round(playerShip.angle/2.5))%360
    if time.time()-invulnTime>invulnLength:
      screen.blit(ships[roundedAngle], (playerShip.rect.x-ships[roundedAngle].get_width()/2,playerShip.rect.y-ships[roundedAngle].get_height()/2))
    else:
      if 10*(round(time.time()-invulnDrawTimer,1))%2==0:
        screen.blit(invulnShips[roundedAngle], (playerShip.rect.x-ships[roundedAngle].get_width()/2,playerShip.rect.y-ships[roundedAngle].get_height()/2))
      else:
        screen.blit(ships[roundedAngle], (playerShip.rect.x-ships[roundedAngle].get_width()/2,playerShip.rect.y-ships[roundedAngle].get_height()/2))
    hyperSpaceCoolBar=pygame.Surface((40,hyperCharge))
    hyperSpaceCoolBar.set_alpha(128)
    hyperSpaceCoolBar.fill(hyperColor)
    screen.blit(hyperSpaceCoolBar,(20,380+(80-hyperCharge)))


  pygame.display.flip()


while running:
    render()
    clock.tick(60)
pygame.quit()
sys.exit()
