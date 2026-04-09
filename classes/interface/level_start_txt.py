import pygame as pg
import constants
from pathlib import Path

# class dedicated to begin a level by displaying a flashing image
# and then triggering the game state running event.

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"

class LevelStartText():
    def __init__(self, lvl_index):
        self.height = constants.SCREEN_HEIGHT
        self.width = constants.SCREEN_WIDTH

        self.lvl_index = lvl_index
        self.surface = pg.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()        

        self.font = pg.font.Font(pixel_font_path, 50)
        
        self.txt_str = f"LEVEL {self.lvl_index}\n START"
        self.txt_surf = self.font.render(self.txt_str, False, 'yellow')
        self.txt_rect = self.txt_surf.get_rect(center=(self.rect.left - 100, self.rect.centery))

        self.txt_speed = 30
        self.isShowing = False

    def move_text(self):
        if self.isShowing:
            self.txt_rect.x += self.txt_speed
            print(self.txt_rect.x)
            print(self.rect.centerx)
           
        if self.txt_rect.center >= (self.rect.centerx, self.rect.centery):
            self.txt_rect.center = (self.rect.centerx, self.rect.centery)
            self.isShowing = False