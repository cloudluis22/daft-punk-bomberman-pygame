import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"
background_path = root_path / "assets" / "graphics" / "backgrounds" / "menu_background.png"
dp_logo_path = root_path / "assets" / "graphics" / "icons" / "dp_logo2.png"
thomas_helmet_path = root_path / "assets" / "graphics" / "icons" / "thomas_menu.png"
guy_helmet_path = root_path / "assets" / "graphics" / "icons" / "guy_menu.png"

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
        self.menu_bg_upscaled = pg.transform.scale2x(self.menu_bg)
        self.menu_logo = pg.image.load(dp_logo_path).convert_alpha()
        self.menu_logo = pg.transform.scale(self.menu_logo, (900, 225))
        self.angle_bg = 0

        self.h_graphic_thomas = pg.image.load(thomas_helmet_path)
        self.h_graphic_thomas = pg.transform.scale_by(self.h_graphic_thomas, 0.4)
        self.h_graphic_thomas_rect = self.h_graphic_thomas.get_rect()

        self.h_graphic_guy = pg.image.load(guy_helmet_path)
        self.h_graphic_guy = pg.transform.scale_by(self.h_graphic_guy, 0.4)
        self.h_graphic_guy_rect = self.h_graphic_guy.get_rect()

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

        self.h_graphic_thomas_rect.left = menu_rect.left + 25
        self.h_graphic_thomas_rect.centery = menu_rect.centery

        self.h_graphic_guy_rect.right = menu_rect.right - 25
        self.h_graphic_guy_rect.centery = menu_rect.centery

        # We draw the background first.
        # rotation logic
        self.angle_bg += 0.05 
        rotating_menu_bg = pg.transform.rotate(self.menu_bg_upscaled, self.angle_bg)
        rotated_menu_rect = rotating_menu_bg.get_rect(center = menu_rect.center)

        menu_surface.blit(rotating_menu_bg, rotated_menu_rect)
        menu_logo_rect = self.menu_logo.get_rect(center=(menu_rect.centerx + 20, menu_rect.centery - 200))
        menu_surface.blit(self.menu_logo, menu_logo_rect)
        menu_surface.blit(self.h_graphic_thomas, self.h_graphic_thomas_rect)
        menu_surface.blit(self.h_graphic_guy, self.h_graphic_guy_rect)

        for element in menu_elements:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            menu_surface.blit(txt_surf, txt_rect)

        return menu_surface, menu_rect       