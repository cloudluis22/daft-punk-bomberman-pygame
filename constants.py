import pygame as pg

################################################################################
# VARIABLES
################################################################################

# These values are in px.
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# TM stands for Tilemap.
TILE_SIZE = 42
TM_WIDTH = 15     
TM_HEIGHT = 13
TM_Y_OFFSET = 30

################################################################################
# GAME STATE
################################################################################
STATE_MENU = "MAIN MENU"
STATE_LVL_START = "LEVEL START"
STATE_GAME = "GAME"
STATE_PAUSE = "PAUSE"
STATE_GAME_OVER = "GAME OVER"

################################################################################
# TRANSITION STATES
################################################################################
T_STATE_IDLE = "IDLE"
T_STATE_FADING_OUT = "FADING_OUT"
T_STATE_BLACKOUT = "BLACKOUT"
T_STATE_FADING_IN = "FADING_IN"

################################################################################
# GAME EVENTS
################################################################################
EV_MENU_SELECTED = pg.event.custom_type()
EV_TRANSITION = pg.event.custom_type()
EV_SCREEN_BLACKOUT = pg.event.custom_type()
EV_MAP_LOADED = pg.event.custom_type()
EV_START_CINEMATIC = pg.event.custom_type()
EV_LEVEL_IGNITE = pg.event.custom_type()
EV_LEVEL_RUN = pg.event.custom_type()
EV_LEVEL_RESUME = pg.event.custom_type()
EV_LEVEL_RESTART = pg.event.custom_type()
EV_LEVEL_QUIT = pg.event.custom_type()
EV_LEVEL_TIME_PASSING = pg.event.custom_type()

################################################################################
# INPUT
################################################################################
INPUT_UP = "UP"
INPUT_DOWN = "DOWN"
INPUT_LEFT = "LEFT"
INPUT_RIGHT = "RIGHT"
INPUT_SELECT = "SELECT"
INPUT_PAUSE = "PAUSE"
INPUT_DROP_BOMB = "DROP_BOMB"

################################################################################
# TILEMAPS
################################################################################
# SCHEME:
## 0: walkable
## 1: solid wall
## 2: solid destructible
## 3: player spawn
## 4: solid wall 2
## 5: v-enemy spawn (THESE TWO WILL HAVE SAME TEXTURE AS WALKABLE)
## 6: h-enemy spawn

TM_LVL1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 2, 0, 2, 0, 2, 0, 6, 2, 0, 2, 0, 3, 1],
[1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 1, 2, 1, 0, 1],
[1, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1],
[1, 2, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1],
[1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1],
[1, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
[1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1],
[1, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 0, 5, 1],
[1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

################################################################################
# TILES ASSETS
################################################################################

TILES_LVL1 = {
    0: 'assets/graphics/tiles/concrete_floor.png',
    1: 'assets/graphics/tiles/concrete_wall.png',
    2: 'assets/graphics/tiles/crate.png',
    3: 'assets/graphics/tiles/spawn.png',
    5: 'assets/graphics/tiles/concrete_floor.png',
    6: 'assets/graphics/tiles/concrete_floor.png' 
}