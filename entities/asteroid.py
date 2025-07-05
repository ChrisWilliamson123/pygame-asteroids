from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT

from helpers.rotation import rotate
from helpers.vectors import angle_to_vector

import math
import pygame
import random

class Asteroid:
    def __init__(self, x, y, velocity):
        self.pos = pygame.Vector2(x, y)
        self.size = random.randint(25, 75)
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.velocity = velocity
        self.rotation_speed = 150
    
    # def rotate(self, direction, dt):
    #     self.heading += direction * self.rotation_speed * dt

    # def thrust(self, dt):
    #     speed = 200
    #     vector = angle_to_vector(self.heading, speed)
    #     new_x = (self.pos.x + (vector.x * dt))
    #     new_y = (self.pos.y + (vector.y * dt))

    #     # Move the ship back into play if it's fully off screen
    #     if self.pos.x > SCREEN_WIDTH and self.pos.x - SCREEN_WIDTH >= self.size:
    #         new_x = 0
    #     if self.pos.x <= -self.size:
    #         new_x = SCREEN_WIDTH - self.size
    #     if self.pos.y > SCREEN_HEIGHT and self.pos.y - SCREEN_HEIGHT >= self.size:
    #         new_y = 0
    #     if self.pos.y <= -self.size:
    #         new_y = SCREEN_HEIGHT - self.size

    #     self.pos.x = new_x
    #     self.pos.y = new_y

    #     # Sync rect to updated float position
    #     self.rect.y = round(self.pos.y)
    #     self.rect.x = round(self.pos.x)
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

    def draw(self, surface):
        pygame.draw.circle(surface, 'white', (self.rect.x + (self.size // 2), self.rect.y + (self.size // 2)), self.size, 1)