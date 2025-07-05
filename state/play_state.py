from gameutils.state.state import State

class PlayState(State):
    def render(self):
        self.screen.fill('black')
