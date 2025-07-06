import math
import random
import pygame

from gameutils.state.state import State

from constants.constants import SCREEN_HEIGHT, SCREEN_WIDTH

from entities.asteroid import Asteroid
from entities.bullet import Bullet
from entities.ship import Ship

from helpers.vectors import angle_to_vector

from sprites.asteroids.asteroid_sprite_name import AsteroidSpriteName
from sprites.asteroids.asteroids_sprite_sheet import AsteroidsSpriteSheet

from state.state_type import StateType

class PlayState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.asteroid_spawn_interval = 2.5
        self.bullet_spawn_interval = 0.25
        sprite_sheet = AsteroidsSpriteSheet()
        self.sprite_surfaces = sprite_sheet.get_sprites()
        ship_sprite_surface = self.sprite_surfaces[AsteroidSpriteName.SHIP]
        self.ship_rotated_top = pygame.transform.rotate(ship_sprite_surface, 90)

        ship_thrusted_sprite_surface = self.sprite_surfaces[AsteroidSpriteName.SHIP_THRUSTED]
        self.ship_thrusted_rotated_top = pygame.transform.rotate(ship_thrusted_sprite_surface, 90)
        self.score = 0

        # Initial state setup
        self.reset()

    def update(self, dt):
        # Add to spawn timers
        self.time_since_last_asteroid += dt
        self.time_since_last_bullet += dt

        # Move bullets
        for bullet in self.bullets_group:
            bullet.move(dt)

        keys = pygame.key.get_pressed()
        # Ship rotation
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-1, dt)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(1, dt)

        # Thrust    
        if keys[pygame.K_UP]:
            self.ship.thrust(dt)
        else:
            self.ship.stop_thrust()

        # Firing
        if keys[pygame.K_SPACE]:
            if self.time_since_last_bullet >= self.bullet_spawn_interval:
                initial_pos_vector = angle_to_vector(self.ship.heading, 75)
                new_x = (self.ship.pos.x + initial_pos_vector.x)
                new_y = (self.ship.pos.y + initial_pos_vector.y)

                continuing_velocity = angle_to_vector(self.ship.heading, 500)
                self.bullets_group.add(Bullet(self.sprite_surfaces[AsteroidSpriteName.BULLET], new_x, new_y, continuing_velocity, self.bullets_group))
                self.time_since_last_bullet = 0
        else:
            # Resetting allows user to fire at will if tapping
            self.time_since_last_bullet = float(math.inf)

        # Move asteroids
        for asteroid in self.asteroids_group:
            asteroid.move(dt)

        # Spawn new asteroid
        if len(self.asteroids_group) < 5 and self.time_since_last_asteroid >= self.asteroid_spawn_interval:
            self.asteroids_group.add(self.spawn_asteroid())
            self.time_since_last_asteroid = 0

        # Collision of ship to asteroids
        if pygame.sprite.spritecollide(self.ship, self.asteroids_group, False):
            if pygame.sprite.spritecollide(self.ship, self.asteroids_group, False, pygame.sprite.collide_mask):
                self.game_manager.change_state(StateType.MAIN_MENU)

        # Collision of bullets to asteroids
        if pygame.sprite.groupcollide(self.bullets_group, self.asteroids_group, False, False):
            if collisions := pygame.sprite.groupcollide(self.bullets_group, self.asteroids_group, True, True, pygame.sprite.collide_mask):
                count = len(collisions)
                self.score += count * 100


    def render(self):
        self.screen.fill('black')

        self.ship_group.draw(self.screen)
        self.asteroids_group.draw(self.screen)
        self.bullets_group.draw(self.screen)

        score_text = self.font_body.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (20, 20))

    def spawn_asteroid(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        x, y = (0, 0)
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
        asteroid_surface = self.sprite_surfaces[asteroid_type]
        size = random.randint(125, 200)
        resized = pygame.transform.smoothscale(asteroid_surface, (size, size))  # width, height in pixels
        return Asteroid(resized, x, y, velocity)

    def reset(self):
        self.time_since_last_asteroid = 0
        self.time_since_last_bullet = 0
        self.build_asteroids_group()
        self.build_ship_group()
        self.bullets_group = pygame.sprite.Group()
        self.score = 0

    def build_ship_group(self):
        self.ship = Ship(self.ship_rotated_top, self.ship_thrusted_rotated_top, (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

    def build_asteroids_group(self):
        self.asteroids_group = pygame.sprite.Group()
        self.asteroids_group.add(self.spawn_asteroid())
