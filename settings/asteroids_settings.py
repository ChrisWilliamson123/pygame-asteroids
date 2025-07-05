from gameutils.game_settings import GameSettings

class AsteroidsSettings(GameSettings):
    def __init__(self):
        self._game_speed_multiplier = 1
        super().__init__()

    def parse_json(self, json_data):
        """Parse the loaded json into the class's properties"""
        super().parse_json(json_data)
        self._game_speed_multiplier = json_data.get('game_speed_multiplier', 1)

    def build_json_dict(self):
        """Construct a dictionary from the class's properties that need to be persisted"""
        super_dict = super().build_json_dict()
        asteroid_dict = {
            'game_speed_multiplier': self._game_speed_multiplier
        }
        return super_dict | asteroid_dict