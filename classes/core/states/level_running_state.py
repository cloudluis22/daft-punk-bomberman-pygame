import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.level_start_txt import LevelStartText
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class LevelRunningState(GameState):
    def __init__(self, game : "Game"):
        self.game = game
        self.can_run = False
        self.can_pause = True

    def on_enter_state(self):
        self.game.level_manager.level_start(self.game.level_index)
        
    def handle_event(self, event):
        if event.type == constants.EV_LEVEL_RUN:
            self.can_run = True
        
        if event.type == constants.EV_LEVEL_TIME_PASSING:
            self.game.level_manager.time -= 1

    def update(self):
        if self.game.input_handler.is_pressed(constants.INPUT_PAUSE):
            if self.can_pause:
                self.game.sound_manager.play_sound("sfx_pause")
                self.game.change_state(constants.STATE_GAME_MENU, True)
        elif self.game.level_manager.victory:
            self.game.sound_manager.play_sound("sfx_victory")
            self.game.change_state(constants.STATE_GAME_MENU, True)
        elif self.game.level_manager.game_over:
            self.game.sound_manager.play_sound("sfx_game_over")
            self.game.change_state(constants.STATE_GAME_MENU, True)                                                                    
                                                                       
    def draw(self, screen):
      if self.can_run:
            self.game.level_manager.update_level()
