import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"

class PauseMenu():
    def __init__(self, sound_manager):
        self.height = constants.SCREEN_HEIGHT / 2   # Half size
        self.width = constants.SCREEN_WIDTH / 2 
        self.sound_manager = sound_manager

        self.surface = pg.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2))
        self.inner_rect = self.surface.get_rect()

        self.font_lg = pg.font.Font(pixel_font_path, 60)
        self.font = pg.font.Font(pixel_font_path, 35)

        self.selected_index = None
        self.mouse_pos = None
        self.canClick = False
        self.mouseMode = False

        self.option_selected = False

        menu_elements_dict = [
            {'text': 'PAUSE', 'font': self.font_lg, 'pos': (self.inner_rect.centerx, self.inner_rect.top + 50), "clickable": False, "index": None},
            {'text': 'RESUME GAME', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery - 50), "clickable": True, "index":0},
            {'text': 'RESTART LEVEL', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery), "clickable": True, "index":1},
            {'text': 'EXIT TO MENU', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery + 50), "clickable": True, "index":2},
        ]

        self.pause_menu_elements_rendered_dict = []
    
        for element in menu_elements_dict:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_surf_selected = element['font'].render(element['text'], False, 'red')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            txt_clickable = element["clickable"]
            txt_index = element["index"]
            self.pause_menu_elements_rendered_dict.append({'text': txt_surf,
                                                     'text_selected':  txt_surf_selected,
                                                     'rect': txt_rect,
                                                     'clickable': txt_clickable,
                                                     'index': txt_index})
            
    def change_selected_index(self, new_index):
        if(new_index != self.selected_index):
            self.sound_manager.play_sound('sfx_menu_hover')
            self.selected_index = new_index

    def handlePauseMenuSelect(self):
        if not self.option_selected:
            match self.selected_index:
                case 0:
                    self.sound_manager.play_sound("sfx_menu_select")
                    self.option_selected = True
                    print("game resumed")
                case 1:
                    print("game restarted")
                case 2:
                    print("quit to menu")

    # functions for increasing, decreasing menu index
    def index_inc(self):
        if(self.selected_index == None):
            self.change_selected_index(0)
        else:
            if(self.selected_index < 2):
                self.change_selected_index(self.selected_index + 1)

    def index_dec(self):
        if(self.selected_index == None):
            self.change_selected_index(0)
        else:
            if(self.selected_index > 0):
                self.change_selected_index(self.selected_index - 1)

    def draw_pause_menu(self):

       # self.surface.fill((0, 0, 0, 230))

        menu_x, menu_y = self.rect.topleft
        self.mouse_pos = pg.mouse.get_pos()

        adjusted_mouse_pos = (self.mouse_pos[0] - menu_x, self.mouse_pos[1] - menu_y)
     
        for element in self.pause_menu_elements_rendered_dict:
            # Must be in mouse mode
            if self.mouseMode:
                # This conditional checks mouse hovering
                if(element["rect"].collidepoint(adjusted_mouse_pos)):
                    # We check if the element is clickable or not
                    if(element["clickable"] == True):
                        self.canClick = True
                        self.change_selected_index(element["index"])
                    else:
                        self.canClick = False
    
            self.surface.blit(element["text"], element["rect"])

            # This checks for the selected index, making the selecting behaviour independent from mouse hovering and button pressing.
            if(self.selected_index != None and self.selected_index == element["index"]):
                self.surface.blit(element["text_selected"], element["rect"]) 
        
        return self.surface, self.rect