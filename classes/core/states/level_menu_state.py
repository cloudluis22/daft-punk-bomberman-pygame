import pygame as pg
import constants
from classes.core.game_state import GameState
from classes.interface.game_menu import GameMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.core.game import Game

class LevelMenuState(GameState):
    def __init__(self, game: "Game"):
        self.game = game
        self.game_menu = GameMenu(game.sound_manager)
        self.menu_state = constants.MENU_VICTORY
        self.quit = False
        self.option_selected = False

    def on_enter_state(self):
        self.quit = False
        self.option_selected = False
        self.game_menu.resize_menu_window(self.menu_state)
      
    def handle_event(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.JOYHATMOTION or  event.type == pg.JOYBUTTONDOWN:
            if not self.option_selected:
                if self.game.input_handler.is_pressed(constants.INPUT_DOWN):
                    self.game_menu.index_inc()
                elif self.game.input_handler.is_pressed(constants.INPUT_UP):
                    self.game_menu.index_dec()
                elif self.game.input_handler.is_pressed(constants.INPUT_SELECT):
                    self.game_menu.handlePauseMenuSelect()

            self.game_menu.mouseMode = False

        # checks if the mouse is placed in a menu option
        elif event.type == pg.MOUSEBUTTONDOWN:
                if self.game_menu.canClick:
                    self.game_menu.handlePauseMenuSelect()
            
        if event.type == pg.MOUSEMOTION:
            self.game_menu.mouseMode = True

        if event.type == constants.EV_LEVEL_RESUME:
            self.game.change_state(constants.STATE_GAME)

        if event.type == constants.EV_LEVEL_RESTART:
            self.option_selected = True
            event = pg.event.Event(
                constants.EV_TRANSITION,
                level_index = self.game.level_index # same index, means restarting
            )
            pg.event.post(event)

        if event.type == constants.EV_LEVEL_QUIT:
            self.option_selected = True
            self.game.sound_manager.stop_music_fadeout()
            self.quit = True
            event = pg.event.Event(
                constants.EV_TRANSITION,
                level_index = 1
            )
            pg.event.post(event)
             
        if event.type == constants.EV_TRANSITION:
            self.game.transition_manager.transition_fade_out()
            self.game.level_index = event.level_index

        if event.type == constants.EV_SCREEN_BLACKOUT:
            self.game.level_manager.unload_level()
            if not self.quit:
                self.game.change_state(constants.STATE_LVL_START, True)
            else:
                self.game.change_state(constants.STATE_MENU, True)

    def update(self):
        if not self.option_selected:
            if self.game.input_handler.is_pressed(constants.INPUT_PAUSE):
                self.game.sound_manager.play_sound("sfx_pause")
                self.game.change_state(constants.STATE_GAME)

    def draw(self, screen):
        surface, rect = self.game_menu.draw_game_menu(self.menu_state)
        screen.blit(surface, rect)