# Base class for game states.
class GameState:

    def on_enter_state(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass