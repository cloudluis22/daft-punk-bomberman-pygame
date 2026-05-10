import pygame as pg
import constants
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

pixel_font_path = root_path / "assets" / "fonts" / "pixel_font.ttf"
game_over_img_path = root_path / "assets" / "graphics" / "etc" / "defeat.png"
victory_img_path = root_path / "assets" / "graphics" / "etc" / "victory.png"
# FIXME: FIX BUGS
class GameMenu():
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

        self.game_over_img = pg.image.load(game_over_img_path)
        self.game_over_img = pg.transform.scale(self.game_over_img, (600, 250))
        self.game_over_img_rect = self.game_over_img.get_rect()
        self.game_over_img_rect.center = (self.inner_rect.centerx + 120, self.inner_rect.top + 220)

        self.victory_img = pg.image.load(victory_img_path)
        self.victory_img = pg.transform.scale(self.victory_img, (600, 250))
        self.victory_img_rect = self.victory_img.get_rect()
        self.victory_img_rect.center = (self.inner_rect.centerx + 120, self.inner_rect.top + 220)

        self.selected_index = None
        self.mouse_pos = None
        self.canClick = False
        self.mouseMode = False

        self.option_selected = False

        self.pause_m_elements_dict = [
            {'text': 'PAUSE', 'font': self.font_lg, 'pos': (self.inner_rect.centerx, self.inner_rect.top + 50), "clickable": False, "index": None},
            {'text': 'RESUME GAME', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery - 50), "clickable": True, "index":0},
            {'text': 'RESTART LEVEL', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery), "clickable": True, "index":1},
            {'text': 'EXIT TO MENU', 'font': self.font, 'pos': (self.inner_rect.centerx, self.inner_rect.centery + 50), "clickable": True, "index":2},
        ]

        self.game_over_m_element_dict = [
            {'text': 'GAME OVER', 'font': self.font_lg, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.top + 50), "clickable": False, "index": None},
            {'text': 'RESTART LEVEL', 'font': self.font, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.centery + 200), "clickable": True, "index":1},
            {'text': 'EXIT TO MENU', 'font': self.font, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.centery + 250), "clickable": True, "index":2},        
        ]

        self.victory_m_element_dict = [
            {'text': 'LEVEL COMPLETED!', 'font': self.font_lg, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.top + 50), "clickable": False, "index": None},
            {'text': 'RESTART LEVEL', 'font': self.font, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.centery + 200), "clickable": True, "index":1},
            {'text': 'EXIT TO MENU', 'font': self.font, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.centery + 250), "clickable": True, "index":2},        
            {'text': 'CONTINUE TO NEXT LEVEL', 'font': self.font, 'pos': (self.inner_rect.centerx + 120, self.inner_rect.centery + 300), "clickable": True, "index": 3},
        ]

        self.game_menu_elements_rendered_dict = []
    
    def resize_menu_window(self, menu_state):
        if menu_state == constants.MENU_PAUSE:
            self.height = constants.SCREEN_HEIGHT / 2   # Half size
            self.width = constants.SCREEN_WIDTH / 2

        if menu_state == constants.MENU_VICTORY or menu_state == constants.MENU_GAME_OVER:
            self.height = int(constants.SCREEN_HEIGHT * 0.75)   # Half size
            self.width = int(constants.SCREEN_WIDTH * 0.75)

        self.surface = pg.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2))
        self.inner_rect = self.surface.get_rect()

        current_elements_dict = []

        match menu_state:
            case constants.MENU_PAUSE:
                current_elements_dict = self.pause_m_elements_dict
            case constants.MENU_VICTORY:
                current_elements_dict = self.victory_m_element_dict
            case constants.MENU_GAME_OVER:
                current_elements_dict = self.game_over_m_element_dict

        for element in current_elements_dict:
            txt_surf = element['font'].render(element['text'], False, 'white')
            txt_surf_selected = element['font'].render(element['text'], False, 'red')
            txt_rect = txt_surf.get_rect(center=element['pos'])
            txt_clickable = element["clickable"]
            txt_index = element["index"]
            self.game_menu_elements_rendered_dict.append({'text': txt_surf,
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
                    event = pg.event.Event(constants.EV_LEVEL_RESUME)
                    pg.event.post(event)
                case 1:
                    self.sound_manager.play_sound("sfx_menu_select")
                    event = pg.event.Event(constants.EV_LEVEL_RESTART)
                    pg.event.post(event)                
                case 2:
                    event = self.sound_manager.play_sound("sfx_menu_select")
                    event = pg.event.Event(constants.EV_LEVEL_QUIT)
                    pg.event.post(event)

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

    def draw_game_menu(self, menu_state):

        menu_x, menu_y = self.rect.topleft
        self.mouse_pos = pg.mouse.get_pos()

        adjusted_mouse_pos = (self.mouse_pos[0] - menu_x, self.mouse_pos[1] - menu_y)
     
        for element in self.game_menu_elements_rendered_dict:
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

        if menu_state == constants.MENU_GAME_OVER:
            self.surface.blit(self.game_over_img, self.game_over_img_rect)
        elif menu_state == constants.MENU_VICTORY:
            self.surface.blit(self.victory_img, self.victory_img_rect)
         
        return self.surface, self.rect