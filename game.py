import pygame
import constants
from sys import exit
from classes.game_environment.sound_manager import SoundManager
from classes.interface.main_menu import MainMenu
from classes.interface.transition_manager import TransitionManager
from classes.game_environment.level_manager import LevelManager

# CONSTANTS
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

# VARIABLES
game_state = constants.STATE_MENU    # Default state.

# INITIAL SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Daft Punk Bomberman")
clock = pygame.time.Clock()

# MANAGERS
sound_manager = SoundManager()
level_manager = LevelManager(screen, game_state, sound_manager)
transition_manager = TransitionManager()  

# MENU
main_menu = MainMenu(level_manager, sound_manager)
menu_surface, menu_rect, menu_canClick = main_menu.draw_menu()

# FLAGS
lvl_loaded = False

while True:

    transition_surface = transition_manager.draw_transition()

    # EVENT HANDLING LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == constants.EV_MENU_SELECTED:
            main_menu.game_started = True

        if event.type == constants.EV_GAME_START_TRANSITION:
            transition_manager.transition_fade_out()
        
        if event.type == constants.EV_LEVEL_LOADED:
            game_state = constants.STATE_LVL_START
        
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
        sound_manager.play_music("mus_menu")

    if(game_state == constants.STATE_LVL_START):
        if(transition_manager.state == constants.T_STATE_BLACKOUT):
            transition_manager.transition_fade_in()
        screen.blit(level_manager.current_bg, (0, 0))
        screen.blit(level_manager.map_surface, (level_manager.offset_x, level_manager.offset_y))
       
    if(game_state == constants.STATE_GAME):
        level_manager.update_level()

    if(transition_manager.state == constants.T_STATE_BLACKOUT):
        if(lvl_loaded == False): # Flag to make sure to do it once
            level_manager.load_level(1)
            lvl_loaded = True
        else:
            pass

    # Blit this only if is not in idle, this should improve performance a tiny bit
    if transition_manager.state != constants.T_STATE_IDLE:
        screen.blit(transition_surface)

    pygame.display.update()
    clock.tick(60)