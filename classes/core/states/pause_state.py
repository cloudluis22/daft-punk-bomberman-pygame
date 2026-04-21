import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.pause_menu import PauseMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class PauseState(GameState):
    def __init__(self, game: "Game"):
        self.game = self.game
        self.pause_menu = PauseMenu(game.sound_manager)
    
    def handle_event(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.JOYHATMOTION or  event.type == pg.JOYBUTTONDOWN:
            if self.game.input_handler.is_pressed(constants.INPUT_DOWN):
                self.pause_menu.index_inc()
            elif self.game.input_handler.is_pressed(constants.INPUT_UP):
                self.pause_menu.index_dec()
            elif self.game.input_handler.is_pressed(constants.INPUT_SELECT):
                self.pause_menu.handlePauseMenuSelect()

            self.menu.mouseMode = False

        # checks if the mouse is placed in a menu option
        elif event.type == pg.MOUSEBUTTONDOWN:
                if self.menu.canClick:
                    self.menu.handlePauseMenuSelect()
            
        if event.type == pg.MOUSEMOTION:
            self.menu.mouseMode = True

    def update(self):
        pass

    def draw(self, screen):
        surface, rect = self.pause_menu.draw_pause_menu()
        screen.blit(surface, rect)