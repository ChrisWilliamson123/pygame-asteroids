from constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from entities.ship import Ship
from entities.asteroid import Asteroid

from gameutils.state.state import State

import random
import pygame

class PlayState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.ship = Ship((SCREEN_WIDTH // 2) - 10, (SCREEN_HEIGHT // 2) - 10)
        self.asteroids = set()
        self.asteroids.add(self.spawn_asteroid())
        self.time_since_last_asteroid = 0
        self.asteroid_spawn_interval = 1

    def spawn_asteroid(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            x = random.uniform(0, SCREEN_WIDTH)
            y = -50
        elif edge == 'bottom':
            x = random.uniform(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 50
        elif edge == 'left':
            x = -50
            y = random.uniform(0, SCREEN_HEIGHT)
        elif edge == 'right':
            x = SCREEN_WIDTH + 50
            y = random.uniform(0, SCREEN_HEIGHT)

        # Aim toward center (with slight randomness)
        center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        direction = pygame.Vector2(center.x - x, center.y - y).normalize()
        direction.rotate_ip(random.uniform(-20, 20))  # Add randomness
        speed = random.uniform(100, 300)
        velocity = direction * speed
        print(x, y)
        return Asteroid(x, y, velocity)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        # Ship rotation
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-1, dt)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(1, dt)
        if keys[pygame.K_UP]:
            self.ship.thrust(dt)

        # Move asteroids
        for asteroid in self.asteroids:
            asteroid.move(dt)

        # Spawn new asteroid
        self.time_since_last_asteroid += dt
        if self.time_since_last_asteroid >= self.asteroid_spawn_interval:
            self.asteroids.add(self.spawn_asteroid())
            self.time_since_last_asteroid = 0

        # Check for asteroid collisions
        new_asteroids = set()
        for asteroid in self.asteroids:
            if self.ship.rect.colliderect(asteroid.rect):
                continue
            new_asteroids.add(asteroid)
        self.asteroids = new_asteroids

    def render(self):
        self.screen.fill('black')

        self.ship.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
