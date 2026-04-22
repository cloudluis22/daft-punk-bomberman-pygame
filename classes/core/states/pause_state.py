import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.pause_menu import PauseMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class PauseState(GameState):
    def __init__(self, game: "Game"):
        self.game = game
        self.pause_menu = PauseMenu(game.sound_manager)
    
    def handle_event(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.JOYHATMOTION or  event.type == pg.JOYBUTTONDOWN:
            if self.game.input_handler.is_pressed(constants.INPUT_DOWN):
                self.pause_menu.index_inc()
            elif self.game.input_handler.is_pressed(constants.INPUT_UP):
                self.pause_menu.index_dec()
            elif self.game.input_handler.is_pressed(constants.INPUT_SELECT):
                self.pause_menu.handlePauseMenuSelect()

            self.pause_menu.mouseMode = False

        # checks if the mouse is placed in a menu option
        elif event.type == pg.MOUSEBUTTONDOWN:
                if self.pause_menu.canClick:
                    self.pause_menu.handlePauseMenuSelect()
            
        if event.type == pg.MOUSEMOTION:
            self.pause_menu.mouseMode = True

    def update(self):
        if self.game.input_handler.is_pressed(constants.INPUT_PAUSE):
            self.game.sound_manager.play_sound("sfx_pause")
            self.game.change_state(constants.STATE_GAME)

    def draw(self, screen):
        surface, rect = self.pause_menu.draw_pause_menu()
        screen.blit(surface, rect)