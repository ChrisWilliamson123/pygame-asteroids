from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT

from helpers.rotation import rotate
from helpers.vectors import angle_to_vector

import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, unthrusted_image, thrusted_image, center_x, center_y):
        super().__init__()

        self.original_unthrusted_image = unthrusted_image  # Unrotated source image
        self.original_thrusted_image = thrusted_image  # Unrotated source image
        self.image = unthrusted_image

        self.pos = pygame.Vector2(center_x, center_y)
        self.rect = self.image.get_rect(center=self.pos)
        self.heading = 0
        self.rotation_speed = 300
        self.speed = 300
        self.thrusting = False
    
    def rotate(self, direction, dt):
        self.heading += direction * self.rotation_speed * dt

        self.sync_image_and_rect()

    def thrust(self, dt):
        if not self.thrusting:
            self.thrusting = True
            self.change_image(self.original_thrusted_image)

        vector = angle_to_vector(self.heading, self.speed)
        new_x = (self.pos.x + (vector.x * dt))
        new_left = new_x - self.half_width
        new_y = (self.pos.y + (vector.y * dt))
        new_top = new_y - self.half_height

        # Move the ship back into play if it's fully off screen
        if new_left > SCREEN_WIDTH and new_left - SCREEN_WIDTH >= self.rect.width:
            new_x = 0 + self.half_width
        if new_left <= -self.rect.width:
            new_x = SCREEN_WIDTH - self.half_width
        if new_top > SCREEN_HEIGHT and new_top - SCREEN_HEIGHT >= self.rect.height:
            new_y = 0 + self.half_height
        if new_top <= -self.rect.height:
            new_y = SCREEN_HEIGHT - self.half_height

        self.pos.x = new_x
        self.pos.y = new_y

        # Sync image and rect to updated float position
        self.sync_image_and_rect()

    def stop_thrust(self):
        if self.thrusting:
            self.thrusting = False
            self.change_image(self.original_unthrusted_image)

    @property
    def half_width(self):
        return self.rect.width // 2

    @property
    def half_height(self):
        return self.rect.width // 2
    
    def change_image(self, image):
        self.image = pygame.transform.rotate(image, -self.heading)
        self.rect = self.image.get_rect(center=self.pos)  
    
    def sync_image_and_rect(self):
        self.image = pygame.transform.rotate(self.original_thrusted_image if self.thrusting else self.original_unthrusted_image, -self.heading)
        self.rect = self.image.get_rect(center=self.pos) 