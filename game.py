import pygame
import constants
from sys import exit
from classes.game_environment.sound_manager import SoundManager
from classes.interface.main_menu import MainMenu
from classes.interface.transition_manager import TransitionManager
from classes.game_environment.level_manager import LevelManager
from classes.interface.level_start_txt import LevelStartText

# CONSTANTS
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

# VARIABLES
game_state = constants.STATE_MENU  # Default state.

# INITIAL SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Daft Punk Bomberman")
clock = pygame.time.Clock()

# MANAGERS
sound_manager = SoundManager()
level_manager = LevelManager(screen, sound_manager)
transition_manager = TransitionManager()  

# MENU
main_menu = MainMenu(level_manager, sound_manager)
menu_surface, menu_rect, menu_canClick = main_menu.draw_menu()

# FLAGS
flag_lvl_loaded = False
flag_start_cinematic = False

# Variables
selected_level_index = 1 # default state
level_start_txt = LevelStartText(selected_level_index)

while True:

    transition_surface = transition_manager.draw_transition()

    # EVENT HANDLING LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # called in main_menu.py when selecting an option
        if event.type == constants.EV_MENU_SELECTED:
            main_menu.game_started = True
            sound_manager.stop_music_fadeout()

        # called in main_menu.py after menu cinematic
        if event.type == constants.EV_GAME_START_TRANSITION:
            transition_manager.transition_fade_out()
            selected_level_index = event.level_index
        
        # called here when game state is LEVEL STARTED
        if event.type == constants.EV_START_CINEMATIC:
            level_start_txt.isShowing = True

        # called in game_manager when load_level is completed.
        if event.type == constants.EV_MAP_LOADED:
            game_state = constants.STATE_LVL_START

        # called after level text dissapears in level_start_txt
        if event.type == constants.EV_LEVEL_IGNITE:
            level_manager.level_start(1)

        # called after level_start in level_manager.py
        if event.type == constants.EV_LEVEL_RUN:
            game_state = constants.STATE_GAME
             
    # I believe I have to add button input for non sprite classes here becasuse
    # they don't have an update method.
        if game_state == constants.STATE_MENU:
            if main_menu.option_selected == False: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        main_menu.index_inc()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        main_menu.index_dec()
                    elif event.key == pygame.K_RETURN:
                        main_menu.handleMenuSelect()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_canClick:
                        main_menu.handleMenuSelect()
    
    # STATE HANDLING LOGIC
    if(game_state == constants.STATE_MENU):
        menu_surface, menu_rect, menu_canClick = main_menu.draw_menu()
        screen.blit(menu_surface, menu_rect)
      
    if(game_state == constants.STATE_LVL_START):
        if(transition_manager.state == constants.T_STATE_BLACKOUT):
            transition_manager.transition_fade_in()
        screen.blit(level_manager.current_bg, (0, 0))
        screen.blit(level_manager.map_surface, (level_manager.offset_x, level_manager.offset_y))
        if flag_start_cinematic == False:
            pygame.time.set_timer(constants.EV_START_CINEMATIC, 1000, loops=1)
            flag_start_cinematic = True

        level_start_txt.move_text()
        screen.blit(level_start_txt.txt_surf, level_start_txt.txt_rect)

    if(game_state == constants.STATE_GAME):
        level_manager.update_level()

    if(transition_manager.state == constants.T_STATE_BLACKOUT):
        if(flag_lvl_loaded == False): # Flag to make sure to do it once
            level_manager.load_level(selected_level_index)
            flag_lvl_loaded = True
        else:
            pass

    # Blit this only if is not in idle, this should improve performance a tiny bit
    if transition_manager.state != constants.T_STATE_IDLE:
        screen.blit(transition_surface)

    print(game_state)
    pygame.display.update()
    clock.tick(60)