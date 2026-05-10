import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

t_lives_i_path = root_path / "assets" / "graphics" / "icons" / "thomas_icon.png"
pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"

def draw_in_hud(self):
    hud_surface = self.image
    inner_rect = hud_surface.get_rect()
    font = self.font
    font_lg = self.font_lg
    lives_icon = self.lives_icon
    lives = self.lives
    score = self.score
    time = self.time

    # We apply the fill again so it re-draws all the surface, preventing text overlap.
    self.image.fill((200, 0, 0, 180))


    hud_elements = [
        {'text': 'Daft Punk Bomberman', 'font': font_lg, 'pos': (inner_rect.centerx, inner_rect.centery - 25)},
        {'text': 'Level 1: Rave à Paris', 'font': font, 'pos': (inner_rect.centerx, inner_rect.centery)},
        {'text': f'X{lives}', 'font': font, 'pos': (inner_rect.left + 80, inner_rect.centery - 20)},
        {'text': f'SCORE: {score}', 'font': font, 'pos': (inner_rect.left + 80, inner_rect.centery + 10)},
        {'text': f'TIME: {time}', 'font': font, 'pos': (inner_rect.right - 80, inner_rect.centery + 10)},
    ]

    for item in hud_elements:
        txt_surf = item['font'].render(item['text'], False, 'white')
        txt_rect = txt_surf.get_rect(center=item['pos'])
        hud_surface.blit(txt_surf, txt_rect)
    
    hud_surface.blit(lives_icon, lives_icon.get_rect(center=(inner_rect.left + 50, inner_rect.centery - 20)))

def update_score(self, hud_elements, new_score):
    hud_surface = self.image
    inner_rect = hud_surface.get_rect()
    font = self.font

    txt_score = hud_elements[3]

    txt_score = font.render(f'SCORE: {new_score}', False,'white')
    txt_rect = txt_score.get_rect(center=(inner_rect.left + 80, inner_rect.centery + 10))
    hud_surface.blit(txt_score, txt_rect)

class HUD(pg.sprite.Sprite):
    def __init__(self, screen, player, score, lives, time):
        super().__init__()
        self.screen = screen
        self.player = player
        self.score = score
        self.lives = lives
        self.time = time

        self.font = pg.font.Font(pixel_font_path, 25)
        self.font_lg = pg.font.Font(pixel_font_path, 35)
        self.lives_icon = pg.image.load(t_lives_i_path).convert_alpha()       
        self.image = pg.Surface((830, 75), pg.SRCALPHA)
        self.image.fill((239, 217, 11, 180))
        self.rect = self.image.get_rect(center=(constants.SCREEN_WIDTH / 2, 50))
        draw_in_hud(self)

    def update(self, current_lives, current_score, current_time):

        # Re-draw HUD ONLY if values change.
        if(self.lives != current_lives):
            self.lives = current_lives
            draw_in_hud(self)

        elif(self.score != current_score):
            self.score = current_score            
            draw_in_hud(self)
        
        elif(self.time != current_time):
            self.time = current_time
            draw_in_hud(self)