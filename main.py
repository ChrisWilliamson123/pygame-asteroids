from constants.constants import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, FRAMERATE
from context.context import Context
from settings.asteroids_settings import AsteroidsSettings

from state.state_type import StateType
from state.main_menu_state import MainMenuState
import state.state_transition_manager as state_transition_manager

from gameutils.game_manager import GameManager

def states_builder(game_manager):
    return {
        StateType.MAIN_MENU: MainMenuState(game_manager)
    }

if __name__ == '__main__':
    settings = AsteroidsSettings()
    context = Context()
    game_manager = GameManager((SCREEN_WIDTH, SCREEN_HEIGHT), CAPTION, states_builder, StateType.MAIN_MENU, state_transition_manager.change_state, context, settings)
    game_manager.run()