from gameutils.sprites.sprite import Sprite
from gameutils.sprites.sprite_sheet import SpriteSheet

from sprites.asteroids.asteroid_sprite_name import AsteroidSpriteName

class AsteroidsSpriteSheet(SpriteSheet):
    def __init__(self):
        file = 'assets/asteroids-2x.png'
        sprites = [
            Sprite(AsteroidSpriteName.LARGE_1, (0, 0), (160, 160)),
            Sprite(AsteroidSpriteName.LARGE_2, (160, 0), (160, 160)),
            Sprite(AsteroidSpriteName.LARGE_3, (320, 0), (160, 160)),
            Sprite(AsteroidSpriteName.SHIP, (192, 256), (96, 64)),
            Sprite(AsteroidSpriteName.SHIP_THRUSTED, (288, 256), (96, 64)),
            Sprite(AsteroidSpriteName.BULLET, (448, 288), (32, 32))
        ]
        super().__init__(file, sprites)
