from constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from entities.ship import Ship

from gameutils.state.state import State

import pygame

class PlayState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.ship = Ship((SCREEN_WIDTH // 2) - 10, (SCREEN_HEIGHT // 2) - 10)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        # Ship rotation
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-1, dt)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(1, dt)
        if keys[pygame.K_UP]:
            self.ship.thrust(dt)

    def render(self):
        self.screen.fill('black')

        self.ship.draw(self.screen)
