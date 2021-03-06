#!/usr/bin/python
import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
screen_width=800
screen_height=800
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
BLUE = (33, 135, 203)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
ORANGE = (225, 102, 31)

class Sprite:
 image = pygame.image.load('cat.png')
 x = 0
 y = 0

 def width(self):
  return self.image.get_width()

 def height(self):
  return self.image.get_height()

 def blit(self, surface):
  surface.blit(self.image, (self.x, self.y))


class Mouse(Sprite):
 image = pygame.image.load('mouse.png')
 


cat = Sprite()

pygame.key.set_repeat(True)

while True: # the main game loop

 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == pygame.KEYDOWN:
   if event.key == pygame.K_LEFT:
    cat.x -= 10
   if event.key == pygame.K_RIGHT:
    cat.x += 10
   if event.key == pygame.K_UP:
    cat.y -= 10
   if event.key == pygame.K_DOWN:
    cat.y += 10

  if cat.x >= screen_width - cat.width() :
   cat.x = screen_width - cat.width()
  if cat.y >= screen_height - cat.height() :
   cat.y = screen_height - cat.height()
  if cat.x <= 0:
   cat.x = 0
  if cat.y <= 0:
   cat.y = 0

 print 'cat = {},{}'.format(cat.x, cat.y)

 screen.fill(TEAL)
 pygame.draw.circle(screen, ORANGE, (screen_width/2, screen_height/2), 30, 0)
 cat.blit(screen)

 pygame.display.update()
 fpsClock.tick(FPS)

