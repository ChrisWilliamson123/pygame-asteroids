from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT

from helpers.rotation import rotate
from helpers.vectors import angle_to_vector

import math
import pygame
import random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, x, y, velocity):
        super().__init__()

        self.original_image = image
        self.image = image.copy()

        self.pos = pygame.Vector2(x, y)
        self.size = self.image.get_width() # asteroids are square
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.velocity = velocity
        self.rotation_speed = 150 # TODO: rotate the asteroid

    def move(self, dt):
        new_x = (self.pos.x + (self.velocity.x * dt))
        new_y = (self.pos.y + (self.velocity.y * dt))

        # Move the asteroid back into play if it's fully off screen
        if new_x > SCREEN_WIDTH and new_x - SCREEN_WIDTH >= self.size:
            new_x = 0
        if new_x <= -self.size:
            new_x = SCREEN_WIDTH - self.size
        if new_y > SCREEN_HEIGHT and new_y - SCREEN_HEIGHT >= self.size:
            new_y = 0
        if new_y <= -self.size:
            new_y = SCREEN_HEIGHT - self.size

        self.pos.x = new_x
        self.pos.y = new_y
        # Sync rect to updated float position
        self.rect.y = round(self.pos.y)
        self.rect.x = round(self.pos.x)