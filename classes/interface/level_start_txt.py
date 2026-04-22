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
        self.txt_rect = self.txt_surf.get_rect(center=(self.rect.left - 2000, self.rect.centery))

        self.txt_speed = 30
        self.isShowing = False
        self.wasShowed = False
        self.isCentered = False
        self.waited = False
        self.timestamp = None
        self.wait_time = 1000

    def move_text(self):
        if self.isShowing:
            self.txt_rect.x += self.txt_speed
            self.timestamp = pg.time.get_ticks()
            
            if self.txt_rect.centerx >= self.rect.centerx:
                self.txt_rect.centerx = self.rect.centerx
                self.isShowing = False
                self.isCentered = True

        if self.isCentered and self.waited == False:
            current_ticks = pg.time.get_ticks()

            if current_ticks - self.timestamp >= self.wait_time:
                self.wasShowed = True
                self.isCentered = False
        
        if self.wasShowed:
            self.txt_rect.x += self.txt_speed

        if self.txt_rect.x >= self.rect.right + 100:
            evt_lvl_ignite = pg.event.Event(constants.EV_LEVEL_IGNITE)
            pg.event.post(evt_lvl_ignite)
            self.txt_rect.x = self.rect.left - 2000
            self.wasShowed = False