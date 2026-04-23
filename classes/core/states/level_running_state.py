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
        self.canRun = False

    def on_enter_state(self):
        self.game.level_manager.level_start(self.game.level_index)
        
    def handle_event(self, event):
        if event.type == constants.EV_LEVEL_RUN:
            self.canRun = True

    def update(self):
        if self.game.input_handler.is_pressed(constants.INPUT_PAUSE):
            self.game.sound_manager.play_sound("sfx_pause")
            self.game.change_state(constants.STATE_PAUSE, True)
                      
    def draw(self, screen):
      if self.canRun:
            self.game.level_manager.update_level()