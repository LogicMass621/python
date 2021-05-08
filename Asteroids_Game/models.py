# Test merge
#Didn't actually code. For ship
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)

class GameObject:
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

class Ship(GameObject):
  Control = 3
  Acceleration = 0.25

  def rotate(self, clockwise=True):
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
