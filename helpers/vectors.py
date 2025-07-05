import math
import pygame

def angle_to_vector(angle, magnitude):
    x_component = magnitude * math.sin(math.radians(angle))
    y_component = -magnitude * math.cos(math.radians(angle))
    return pygame.Vector2(x_component, y_component)