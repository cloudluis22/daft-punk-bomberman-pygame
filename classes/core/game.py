import pygame as pg
import constants
from sys import exit
import pygame as pg
from pathlib import Path

from classes.core.input_handler import InputHandler
from classes.game_environment.sound_manager import SoundManager
from classes.game_environment.level_manager import LevelManager
from classes.interface.transition_manager import TransitionManager

from classes.core.states.menu_state import MenuState
from classes.core.states.level_start_state import LevelStartState
from classes.core.states.level_running_state import LevelRunningState
from classes.core.states.level_menu_state import LevelMenuState

current_path = Path(__file__).parent
root_path = current_path.parent.parent

icon_path = root_path / "assets" / "graphics" / "icons" / "app_icon.png"

# This class serves as a core class that handles all game behaviour in a single
# easily accesible class, allowing for easier feature implementations.
class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.app_icon = pg.image.load(icon_path).convert_alpha()
        pg.display.set_caption("Daft Punk Bomberman")
        pg.display.set_icon(self.app_icon)
        self.clock = pg.time.Clock()

        self.input_handler = InputHandler()
        self.sound_manager = SoundManager()
        self.level_manager = LevelManager(self.screen, self.sound_manager, self.input_handler)
        self.transition_manager = TransitionManager()

        self.level_index = 1 

        self.game_states_dict = {
            constants.STATE_MENU: MenuState(self),
            constants.STATE_LVL_START: LevelStartState(self),
            constants.STATE_GAME: LevelRunningState(self),
            constants.STATE_GAME_MENU: LevelMenuState(self)
        }

        # Initialized default with the first state.
        self.current_state = self.game_states_dict[constants.STATE_MENU]
        self.current_state.on_enter_state()
        self.events= {}
    
    def change_state(self, new_state, do_on_enter=False):
        self.current_state = self.game_states_dict[new_state]
        if do_on_enter:
            self.current_state.on_enter_state()
    
    def run(self):
        while True:
            # ---- EVENTS ----
            events = pg.event.get()
            self.input_handler.update(events)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()                
                self.current_state.handle_event(event)
            
            # ---- UPDATE ----
            self.current_state.update()

            # ---- DRAW ----
            self.current_state.draw(self.screen)
            
            if self.transition_manager.state != constants.T_STATE_IDLE:
                transition_surface = self.transition_manager.draw_transition()
                self.screen.blit(transition_surface, (0, 0))

            pg.display.update()
            self.clock.tick(60)