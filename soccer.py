#!/usr/bin/python
import pygame, sys, random
from pygame.locals import *
FPS = 60
screen_width=1200
screen_height=1000
class Sprite:
 image path = 'soccerBall.ping'

 def __init__(self):
  self.image = pygame.image.load(self.image_path)

