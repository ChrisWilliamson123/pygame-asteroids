import pygame

from constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, velocity, group):
        super().__init__()

        self.original_image = image
        self.image = image
        self.pos = pygame.Vector2(x, y)

        self.rect = self.image.get_rect(center=self.pos)
        self.velocity = velocity
        self.group = group

    def move(self, dt):
        new_x = (self.pos.x + (self.velocity.x * dt))
        new_y = (self.pos.y + (self.velocity.y * dt))

        # Move the asteroid back into play if it's fully off screen
        # if new_x > SCREEN_WIDTH and new_x - SCREEN_WIDTH >= self.size:
        #     new_x = 0
        # if new_x <= -self.size:
        #     new_x = SCREEN_WIDTH - self.size
        # if new_y > SCREEN_HEIGHT and new_y - SCREEN_HEIGHT >= self.size:
        #     new_y = 0
        # if new_y <= -self.size:
        #     new_y = SCREEN_HEIGHT - self.size

        self.pos.x = new_x
        self.pos.y = new_y

        if (not 0 < self.pos.x < SCREEN_WIDTH) or (not 0 < self.pos.y < SCREEN_HEIGHT):
            self.remove(self.group)

        self.rect = self.image.get_rect(center=self.pos)
