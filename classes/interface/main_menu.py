import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"



class MainMenu():
    def __init__(self):
        self.height = constants.SCREEN_HEIGHT
        self.width = constants.SCREEN_WIDTH
        self.surface = pg.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.surface.fill("black")
        self.font = pg.font.Font(pixel_font_path, 40)

    def draw_menu(self):
        menu_surface = self.surface
        menu_rect = self.rect
        font = self.font

        menu_elements = [
            {'text': 'START GAME', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery - 50)},
            {'text': 'LEVEL SELECT', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery)},
            {'text': f'EXIT', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery + 50)},
        ]

        for element in menu_elements:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            menu_surface.blit(txt_surf, txt_rect)

        return menu_surface, menu_rect       
        

