from state.state_type import StateType

from gameutils.state.state import State
from gameutils.menu_provider.menu_provider import MenuProvider, MenuEntry, Menu, MenuEntryAction

import pygame

class MainMenuState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        menu_entries = [
            MenuEntry(lambda: 'Play', [MenuEntryAction(pygame.K_RETURN, lambda: self.game_manager.change_state(StateType.PLAY))]),
            # MenuEntry(lambda: 'Settings', [MenuEntryAction(pygame.K_RETURN, lambda: self.game_manager.change_state(StateType.SETTINGS))]),
        ]
        menu = Menu('Asteroids', menu_entries)
        menu_provider = MenuProvider(menu, self.font_title, self.font_body, should_flash_selected=False)
        self.add_component(menu_provider)

    def render(self):
        self.screen.fill('black')

        super().render()
