import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.level_start_txt import LevelStartText
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class LevelStartState(GameState):
    def __init__(self, game : "Game"):
        self.game = game
        self.hasLoadedLevel = False
        self.lvlStartTxt = LevelStartText(self.game.level_index)

    def on_enter_state(self):
        self.hasLoadedLevel = False
        self.game.level_manager.load_level(self.game.level_index)
        
    def handle_event(self, event):
        if event.type == constants.EV_MAP_LOADED:
            self.hasLoadedLevel = True
            self.game.transition_manager.transition_fade_in()
            self.lvlStartTxt.isShowing = True

        if event.type == constants.EV_LEVEL_IGNITE:
            self.game.change_state(constants.STATE_GAME, True)

    def update(self):
        self.lvlStartTxt.move_text()            
        pass
    
    def draw(self, screen):
        if self.hasLoadedLevel:
            offset_x = self.game.level_manager.offset_x
            offset_y = self.game.level_manager.offset_y
            screen.blit(self.game.level_manager.current_bg, (0, 0))
            screen.blit(self.game.level_manager.map_surface, (offset_x, offset_y))
            screen.blit(self.lvlStartTxt.txt_surf, self.lvlStartTxt.txt_rect)
        