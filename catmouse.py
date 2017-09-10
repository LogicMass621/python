#!/usr/bin/python
import pygame, sys, random
from pygame.locals import *

class Direction:
 left, right, up, down = range(1,5)

print 'left={}, right={}, up={}, down={}'.format(Direction.left, Direction.right, Direction.up, Direction.down)
pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
screen_width=800
screen_height=800
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('Animation')
sprite_speed=10

WHITE = (255, 255, 255)
BLUE = (33, 135, 203)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
ORANGE = (225, 102, 31)

random.seed()

class Sprite:
 image = pygame.image.load('cat.png')
 x = 0
 y = 0

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

class Mouse(Sprite):
 image = pygame.image.load('mouse.png')
 direction = Direction.right
 counter = 0
 
 def animate(self):
  if self.counter == 0:
   self.counter = random.randint(20,30)
   self.direction = random.randint(1,4)
   print 'counter = {} direction = {}'.format(self.counter, self.direction)

  self.counter -= 1

  if self.direction == Direction.right:
   self.movex(sprite_speed)
   if self.x >= screen_width - self.width():
    self.counter = 0
  elif self.direction == Direction.down:
   self.movey(sprite_speed)
   if self.y >= screen_height - self.height():
    self.counter = 0
  elif self.direction == Direction.left:
   self.movex(-sprite_speed)
   if self.x == 0:
    self.counter = 0
  elif self.direction == Direction.up:
   self.movey(-sprite_speed)
   if self.y == 0:
    self.counter = 0
 
cat = Sprite()
mouse = Mouse()
mouse.x = screen_width-mouse.width()-10
mouse.y = screen_height-mouse.height()-10

pygame.key.set_repeat(True)

while True: # the main game loop

 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_LEFT:
    cat.movex(-sprite_speed)
   if event.key == pygame.K_RIGHT:
    cat.movex(sprite_speed)
   if event.key == pygame.K_UP:
    cat.movey(-sprite_speed)
   if event.key == pygame.K_DOWN:
    cat.movey(sprite_speed)

 mouse.animate()

 print 'cat = {},{} mouse = {},{}'.format(cat.x, cat.y, mouse.x, mouse.y)

 screen.fill(TEAL)
 pygame.draw.circle(screen, ORANGE, (screen_width/2, screen_height/2), 30, 0)
 mouse.blit(screen)
 cat.blit(screen)

 pygame.display.update()
 fpsClock.tick(FPS)

