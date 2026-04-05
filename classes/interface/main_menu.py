import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"
background_path = root_path / "assets" / "graphics" / "backgrounds" / "menu_background.png"
dp_logo_path = root_path / "assets" / "graphics" / "icons" / "dp_logo2.png"

class MainMenu():
    def __init__(self):
        self.height = constants.SCREEN_HEIGHT
        self.width = constants.SCREEN_WIDTH
        self.surface = pg.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.font = pg.font.Font(pixel_font_path, 40)
        self.font_lg = pg.font.Font(pixel_font_path, 80)
        self.font_sm = pg.font.Font(pixel_font_path, 20)
        self.menu_bg = pg.image.load(background_path).convert_alpha()
        self.menu_logo = pg.image.load(dp_logo_path).convert_alpha()
        self.menu_logo = pg.transform.scale(self.menu_logo, (900, 225))

    def draw_menu(self):
        menu_surface = self.surface
        menu_rect = self.rect
        font = self.font
        font_lg = self.font_lg
        font_sm = self.font_sm

        menu_elements = [
            {'text': 'BOMBERMAN', 'font': font_lg, 'pos': (menu_rect.centerx, menu_rect.centery - 60)},
            {'text': 'START GAME', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery + 50)},
            {'text': 'LEVEL SELECT', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery + 100)},
            {'text': 'EXIT', 'font': font, 'pos': (menu_rect.centerx, menu_rect.centery + 150)},
            {'text': 'COPYRIGHT© MMXXVI - JOSÉ LUIS ÁVILA JUÁREZ - GRAFICACIÓN', 'font': font_sm, 'pos': (menu_rect.centerx, menu_rect.bottom - 30)},
        ]

        # We draw the background first.
        menu_surface.blit(self.menu_bg, (0, 0))
        menu_logo_rect = self.menu_logo.get_rect(center=(menu_rect.centerx + 20, menu_rect.centery - 200))
        menu_surface.blit(self.menu_logo, menu_logo_rect)

        for element in menu_elements:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            menu_surface.blit(txt_surf, txt_rect)

        return menu_surface, menu_rect       