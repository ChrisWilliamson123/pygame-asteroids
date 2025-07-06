import random
import pygame

from gameutils.state.state import State

from constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH

from entities.ship import Ship
from entities.asteroid import Asteroid

from sprites.asteroids.asteroid_sprite_name import AsteroidSpriteName
from sprites.asteroids.asteroids_sprite_sheet import AsteroidsSpriteSheet

from state.state_type import StateType

class PlayState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.asteroid_spawn_interval = 5
        sprite_sheet = AsteroidsSpriteSheet()
        self.sprite_surfaces = sprite_sheet.get_sprites()
        ship_sprite_surface = self.sprite_surfaces[AsteroidSpriteName.SHIP]
        self.ship_rotated_top = pygame.transform.rotate(ship_sprite_surface, 90)

        # Initial state setup
        self.reset()

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
        for asteroid in self.asteroids_group:
            asteroid.move(dt)

        # Spawn new asteroid
        self.time_since_last_asteroid += dt
        if len(self.asteroids_group) < 5 and self.time_since_last_asteroid >= self.asteroid_spawn_interval:
            self.asteroids_group.add(self.spawn_asteroid())
            self.time_since_last_asteroid = 0

        if pygame.sprite.spritecollide(self.ship, self.asteroids_group, False):
            if pygame.sprite.spritecollide(self.ship, self.asteroids_group, False, pygame.sprite.collide_mask):
                self.game_manager.change_state(StateType.MAIN_MENU)

    def render(self):
        self.screen.fill('black')

        self.ship_group.draw(self.screen)
        self.asteroids_group.draw(self.screen)

    def spawn_asteroid(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        x, y = 0
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
        center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        direction = pygame.Vector2(center.x - x, center.y - y).normalize()
        direction.rotate_ip(random.uniform(-20, 20))  # Add randomness
        speed = random.uniform(100, 300)
        velocity = direction * speed
        asteroid_type = random.choice([AsteroidSpriteName.LARGE_1, AsteroidSpriteName.LARGE_2, AsteroidSpriteName.LARGE_3])
        return Asteroid(self.sprite_surfaces[asteroid_type], x, y, velocity)

    def reset(self):
        self.time_since_last_asteroid = 0
        self.build_asteroids_group()
        self.build_ship_group()

    def build_ship_group(self):
        self.ship = Ship(self.ship_rotated_top, (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

    def build_asteroids_group(self):
        self.asteroids_group = pygame.sprite.Group()
        self.asteroids_group.add(self.spawn_asteroid())
