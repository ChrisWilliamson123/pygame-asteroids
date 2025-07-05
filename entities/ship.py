from helpers.rotation import rotate

import pygame

class Ship:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.calculate_vertices()

    def calculate_vertices(self):
        vertices = []
        center = self.rect.center
        top = (center[0], center[1] - (self.size // 2))
        vertices.append(top)
        top = rotate(center, top, 120)
        vertices.append(top)
        top = rotate(center, top, 120)
        vertices.append(top)
        self.vertices = vertices

    def draw(self, surface):
        pygame.draw.polygon(surface, 'white', self.vertices)