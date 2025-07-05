from gameutils.state.state import State

class MainMenuState(State):
    def render(self):
        self.screen.fill('black')
