#!/usr/bin/python
import pygame, sys, random
from pygame.locals import *

# GLOBAL VARIABLES
DEBUG = False
FPS = 60 # frames per second setting
screen_width=1200
screen_height=1000

class Direction:
 N,NE,E,SE,S,SW,W,NW = range(1,9)

class Sprite:
 image_path = 'cat.png'
 speed=10*30/FPS
 x = 0
 y = 0

 def __init__(self):
  self.image = pygame.image.load(self.image_path)
  self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
  if DEBUG:
   print 'rect = {}'.format(self.rect)
 
 def movex(self, x):
  self.x += x
  if self.x >= screen_width - self.width() :
   self.x = screen_width - self.width()
   return False
  elif self.x <= 0 :
   self.x = 0
   return False
  return True

 def movey(self, y):
  self.y += y
  if self.y >= screen_height - self.height() :
   self.y = screen_height - self.height()
   return False
  elif self.y <= 0:
   self.y = 0
   return False
  return True

 def width(self):
  return self.image.get_width()

 def height(self):
  return self.image.get_height()

 def blit(self, surface):
  surface.blit(self.image, (self.x, self.y))

 def collided(self, sprite):
   rect1 = Rect(self.x, self.y, self.width(), self.height())
   rect2 = Rect(sprite.x, sprite.y, sprite.width(), sprite.height())
   return rect1.colliderect(rect2)

class Mouse(Sprite):
 image_path = 'mouse.png'
 direction = Direction.E
 counter = 0
 speed = 15*30/FPS
 
 def __init__(self):
  Sprite.__init__(self)
  self.x = screen_width-self.width()-10
  self.y = screen_height-self.height()-10

 def reset(self):
  self.x = random.randint(10, screen_width-self.width()-10)
  self.y = random.randint(10, screen_height-self.height()-10)

 def movex(self, x):
  ret = Sprite.movex(self, x)
  if not ret:
   self.counter = 0
  return ret

 def movey(self, y):
  ret = Sprite.movey(self, y)
  if not ret:
   self.counter = 0
  return ret

 def animate(self):
  if self.counter == 0:
   self.counter = random.randint(30,80)
   self.direction = random.randint(1,8)
   if DEBUG:
    print 'counter = {} direction = {}'.format(self.counter, self.direction)

  self.counter -= 1

  if self.direction == Direction.N:
   self.movey(-self.speed)
  elif self.direction == Direction.NE:
   self.movex(self.speed*2/3)
   self.movey(-self.speed*2/3)
  elif self.direction == Direction.E:
   self.movex(self.speed)
  elif self.direction == Direction.SE:
   self.movex(self.speed*2/3)
   self.movey(self.speed*2/3)
  elif self.direction == Direction.S:
   self.movey(self.speed)
  elif self.direction == Direction.SW:
   self.movex(-self.speed*2/3)
   self.movey(self.speed*2/3)
  elif self.direction == Direction.W:
   self.movex(-self.speed)
  elif self.direction == Direction.NW:
   self.movex(-self.speed*2/3)
   self.movey(-self.speed*2/3)

def main():

 pygame.init()

 clock = pygame.time.Clock()

 # set up the window
 screen = pygame.display.set_mode([screen_width, screen_height])

 points = 0

 WHITE = (255, 255, 255)
 BLUE = (33, 135, 203)
 SILVER = (192, 192, 192)
 TEAL = (0, 128, 128)
 ORANGE = (225, 102, 31)

 random.seed()

 cat = Sprite()
 mouse = Mouse()

 pygame.key.set_repeat(True)

 # MAIN GAME LOOP
 while True:

 # 1. GET DATA
  for event in pygame.event.get():
   if event.type == QUIT:
    pygame.quit()
    sys.exit()
   elif event.type == pygame.KEYDOWN:
    if event.key == pygame.K_LEFT:
     cat.movex(-cat.speed)
    if event.key == pygame.K_RIGHT:
     cat.movex(cat.speed)
    if event.key == pygame.K_UP:
     cat.movey(-cat.speed)
    if event.key == pygame.K_DOWN:
     cat.movey(cat.speed)
    if event.key == pygame.K_ESCAPE:
     pygame.quit()

  # 2. PROCESS DATA
  mouse.animate()

  if cat.collided(mouse):
    points += 1
    mouse.reset()

  if DEBUG:
   print 'cat = {},{} mouse = {},{} points = {}'.format(cat.x, cat.y, mouse.x, mouse.y, points)

  # 3. OUTPUT DATA
  screen.fill(TEAL)
  pygame.draw.circle(screen, ORANGE, (screen_width/2, screen_height/2), 30, 0)
  mouse.blit(screen)
  cat.blit(screen)

  pygame.display.flip()
  clock.tick(FPS)
  pygame.display.set_caption("fps: " + str(round(clock.get_fps(),1))+" points: " + str(points))

main()

