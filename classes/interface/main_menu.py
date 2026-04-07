import pygame as pg
import constants
from pathlib import Path
from sys import exit

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"
background_path = root_path / "assets" / "graphics" / "backgrounds" / "menu_background.png"
dp_logo_path = root_path / "assets" / "graphics" / "icons" / "dp_logo2.png"
thomas_helmet_path = root_path / "assets" / "graphics" / "icons" / "thomas_menu.png"
guy_helmet_path = root_path / "assets" / "graphics" / "icons" / "guy_menu.png"

class MainMenu():
    def __init__(self, sound_manager, ev_menu_selected):
        self.height = constants.SCREEN_HEIGHT
        self.width = constants.SCREEN_WIDTH
        self.sound_manager = sound_manager

        self.surface = pg.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()

        self.font = pg.font.Font(pixel_font_path, 40)
        self.font_lg = pg.font.Font(pixel_font_path, 80)
        self.font_sm = pg.font.Font(pixel_font_path, 20)

        self.menu_bg = pg.image.load(background_path).convert_alpha()
        self.menu_bg_upscaled = pg.transform.scale2x(self.menu_bg)
        self.menu_logo = pg.image.load(dp_logo_path).convert_alpha()
        self.menu_logo = pg.transform.scale(self.menu_logo, (900, 225))
        self.menu_logo_rect = self.menu_logo.get_rect(center=(self.rect.centerx + 20, self.rect.centery - 200))
        self.angle_bg = 0

        self.selected_index = None
        self.mouse_pos = None

        self.option_selected = False # Purpose: prevent any more input once an option is choosed
        self.ev_menu_selected = ev_menu_selected

        self.h_graphic_thomas = pg.image.load(thomas_helmet_path).convert_alpha()
        self.h_graphic_thomas = pg.transform.scale_by(self.h_graphic_thomas, 0.4)

        self.h_graphic_thomas_rect = self.h_graphic_thomas.get_rect()
        self.h_graphic_thomas_rect.left = self.rect.left + 25
        self.h_graphic_thomas_rect.centery = self.rect.centery

        self.h_graphic_guy = pg.image.load(guy_helmet_path).convert_alpha()
        self.h_graphic_guy = pg.transform.scale_by(self.h_graphic_guy, 0.4)

        self.h_graphic_guy_rect = self.h_graphic_guy.get_rect()
        self.h_graphic_guy_rect.right = self.rect.right - 25
        self.h_graphic_guy_rect.centery = self.rect.centery

        menu_elements_dict = [
            {'text': 'BOMBERMAN', 'font': self.font_lg, 'pos': (self.rect.centerx, self.rect.centery - 60), "clickable": False, "index": None},
            {'text': 'START GAME', 'font': self.font, 'pos': (self.rect.centerx, self.rect.centery + 50), "clickable": True, "index":0},
            {'text': 'LEVEL SELECT', 'font': self.font, 'pos': (self.rect.centerx, self.rect.centery + 100), "clickable": True, "index":1},
            {'text': 'EXIT', 'font': self.font, 'pos': (self.rect.centerx, self.rect.centery + 150), "clickable": True, "index":2},
            {'text': 'COPYRIGHT© MMXXVI - JOSÉ LUIS ÁVILA JUÁREZ - GRAFICACIÓN', 'font': self.font_sm, 'pos': (self.rect.centerx, self.rect.bottom - 30), "clickable": False, "index": None},
        ]

        self.menu_elements_rendered_dict = []

        for element in menu_elements_dict:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_surf_selected = element['font'].render(element['text'], False, 'red')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            txt_clickable = element["clickable"]
            txt_index = element["index"]
            self.menu_elements_rendered_dict.append({'text': txt_surf,
                                                     'text_selected':  txt_surf_selected,
                                                     'rect': txt_rect,
                                                     'clickable': txt_clickable,
                                                     'index': txt_index})

    # Had to make this function purely for avoiding the sfx play itself infinitely
    def change_selected_index(self, new_index):
        if(new_index != self.selected_index):
            self.sound_manager.play_sound('sfx_menu_hover')
            self.selected_index = new_index

    def handleMenuSelect(self):
        match self.selected_index:
            case 0:
                self.sound_manager.play_sound("sfx_menu_select")
                self.option_selected = True
                pg.time.set_timer(self.ev_menu_selected, 1000, loops=1)
            case 2:
                pg.quit()
                exit()

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

    def draw_menu(self):
        menu_surface = self.surface
        menu_rect = self.rect
        self.mouse_pos = pg.mouse.get_pos()
        canClick = False

        # We draw the background first.
        # rotation logic
        self.angle_bg += 0.05 
        rotating_menu_bg = pg.transform.rotate(self.menu_bg_upscaled, self.angle_bg)
        rotated_menu_rect = rotating_menu_bg.get_rect(center = menu_rect.center)

        # blitting all the grpahical stuff
        menu_surface.blit(rotating_menu_bg, rotated_menu_rect)
        menu_surface.blit(self.menu_logo, self.menu_logo_rect)
        menu_surface.blit(self.h_graphic_thomas, self.h_graphic_thomas_rect)
        menu_surface.blit(self.h_graphic_guy, self.h_graphic_guy_rect)

        # blitting text
        for element in self.menu_elements_rendered_dict:

            # This conditional checks mouse hovering
            if(element["rect"].collidepoint(self.mouse_pos)):
                # We check if the element is clickable or not
                if(element["clickable"] == True):
                    canClick = True
                    self.change_selected_index(element["index"])

            menu_surface.blit(element["text"], element["rect"])

            # This checks for the selected index, making the selecting behaviour independent from mouse hovering and button pressing.
            if(self.selected_index != None and self.selected_index == element["index"]):
                menu_surface.blit(element["text_selected"], element["rect"])
                
        return menu_surface, menu_rect, canClick          
