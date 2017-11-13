#!/usr/bin/python
import pygame, sys, random
from pygame.locals import *

class Direction:
 N,NE,E,SE,S,SW,W,NW = range(1,9)

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
screen_width=800
screen_height=800
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('Animation')

points = 0

WHITE = (255, 255, 255)
BLUE = (33, 135, 203)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
ORANGE = (225, 102, 31)

random.seed()

class Sprite:
 image_path = 'cat.png'
 speed=10
 x = 0
 y = 0

 def __init__(self):
  self.image = pygame.image.load(self.image_path)
  self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
  print 'rect = {}'.format(self.rect)
 
 def movex(self, x):
  self.x += x
  if self.x >= screen_width - self.width() :
   self.x = screen_width - self.width()
  elif self.x <= 0 :
   self.x = 0

 def movey(self, y):
  self.y += y
  if self.y >= screen_height - self.height() :
   self.y = screen_height - self.height()
  elif self.y <= 0:
   self.y = 0

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
 speed = 15
 
 def __init__(self):
  Sprite.__init__(self)
  self.x = screen_width-self.width()-10
  self.y = screen_height-self.height()-10

 def reset(self):
  self.x = random.randint(10, screen_width-self.width()-10)
  self.y = random.randint(10, screen_height-self.height()-10)

 def animate(self):
  if self.counter == 0:
   self.counter = random.randint(20,30)
   self.direction = random.randint(1,8)
   print 'counter = {} direction = {}'.format(self.counter, self.direction)

  self.counter -= 1

  if self.direction == Direction.N:
   self.movey(-self.speed)
   if self.y <= 0:
    self.counter = 0
  elif self.direction == Direction.NE:
   self.movex(self.speed*2/3)
   self.movey(-self.speed*2/3)
   if self.x >= screen_width - self.width() or self.y <= 0:
    self.counter = 0
  elif self.direction == Direction.E:
   self.movex(self.speed)
   if self.x >= screen_width - self.width():
    self.counter = 0
  elif self.direction == Direction.SE:
   self.movex(self.speed*2/3)
   self.movey(self.speed*2/3)
   if self.x >= screen_width - self.width() or self.y >= screen_height - self.height():
    self.counter = 0
  elif self.direction == Direction.S:
   self.movey(self.speed)
   if self.y >= screen_height - self.height():
    self.counter = 0
  elif self.direction == Direction.SW:
   self.movex(-self.speed*2/3)
   self.movey(self.speed*2/3)
   if self.x <= 0 or self.y >= screen_height - self.height():
    self.counter = 0
  elif self.direction == Direction.W:
   self.movex(-self.speed)
   if self.x == 0:
    self.counter = 0
  elif self.direction == Direction.NW:
   self.movex(-self.speed*2/3)
   self.movey(-self.speed*2/3)
   if self.x <= 0 or self.y <= 0:
    self.counter = 0

cat = Sprite()
mouse = Mouse()

pygame.key.set_repeat(True)

while True: # the main game loop

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

 mouse.animate()

 if cat.collided(mouse):
   points += 1
   mouse.reset()

 print 'cat = {},{} mouse = {},{} points = {}'.format(cat.x, cat.y, mouse.x, mouse.y, points)

 screen.fill(TEAL)
 pygame.draw.circle(screen, ORANGE, (screen_width/2, screen_height/2), 30, 0)
 mouse.blit(screen)
 cat.blit(screen)

 pygame.display.update()
 fpsClock.tick(FPS)

