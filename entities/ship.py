from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT

from helpers.rotation import rotate
from helpers.vectors import angle_to_vector

import math
import pygame

class Ship:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.heading = 0
        self.rotation_speed = 150

    def calculate_vertices(self, center):
        vertices = []
        top = (center[0], center[1] - (self.size // 2))
        top = rotate(center, top, self.heading)
        vertices.append(top)
        top = rotate(center, top, 120)
        vertices.append(top)
        top = rotate(center, top, 60)
        vertices.append(top)
        top = rotate(center, top, 60)
        vertices.append(top)
        return vertices
    
    def calculate_bounding_vertices(self):
        return [
            (self.pos.x, self.pos.y),
            (self.pos.x + self.size, self.pos.y),
            (self.pos.x + self.size, self.pos.y + self.size),
            (self.pos.x, self.pos.y + self.size),
        ]
    
    def rotate(self, direction, dt):
        self.heading += direction * self.rotation_speed * dt

    def thrust(self, dt):
        speed = 200
        vector = angle_to_vector(self.heading, speed)
        new_x = (self.pos.x + (vector.x * dt))
        new_y = (self.pos.y + (vector.y * dt))

        # Move the ship back into play if it's fully off screen
        if self.pos.x > SCREEN_WIDTH and self.pos.x - SCREEN_WIDTH >= self.size:
            new_x = 0
        if self.pos.x <= -self.size:
            new_x = SCREEN_WIDTH - self.size
        if self.pos.y > SCREEN_HEIGHT and self.pos.y - SCREEN_HEIGHT >= self.size:
            new_y = 0
        if self.pos.y <= -self.size:
            new_y = SCREEN_HEIGHT - self.size

        self.pos.x = new_x
        self.pos.y = new_y

        # Sync rect to updated float position
        self.rect.y = round(self.pos.y)
        self.rect.x = round(self.pos.x)

    def draw_overflow(self, surface):
        should_overflow_x = abs(self.rect.x - SCREEN_WIDTH) < self.size
        should_overflow_y = abs(self.rect.y - SCREEN_HEIGHT) < self.size

        center = (
            ((self.rect.x - SCREEN_WIDTH) if should_overflow_x else self.rect.x) + (self.size // 2),
            ((self.rect.y - SCREEN_HEIGHT) if should_overflow_y else self.rect.y)  + (self.size // 2),
        )
        
        pygame.draw.polygon(surface, 'white', self.calculate_vertices(center))
            

    def draw(self, surface):
        pygame.draw.polygon(surface, 'white', self.calculate_vertices(self.rect.center))
        pygame.draw.polygon(surface, 'red', self.calculate_bounding_vertices(), 1)