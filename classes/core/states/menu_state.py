import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.main_menu import MainMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class MenuState(GameState):
    def __init__(self, game: "Game"):
        self.game = game
        self.menu = MainMenu(game.sound_manager)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_DOWN, pg.K_s):
                self.menu.index_inc()
            elif event.key in (pg.K_UP, pg.K_w):
                self.menu.index_dec()
            elif event.key == pg.K_RETURN:
                self.menu.handleMenuSelect()
    
        # checks if the mouse is placed in a menu option
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.menu.canClick:
                self.menu.handleMenuSelect()

        if event.type == constants.EV_MENU_SELECTED:
            self.menu.game_started = True
            self.game.sound_manager.stop_music_fadeout()

        if event.type == constants.EV_TRANSITION:
            self.game.transition_manager.transition_fade_out()
            self.game.level_index = event.level_index

        if event.type == constants.EV_SCREEN_BLACKOUT:
            self.game.change_state(constants.STATE_LVL_START)
            
    def update(self):
        pass
    
    def draw(self, screen):
        surface, rect = self.menu.draw_menu()
        screen.blit(surface, rect)
        