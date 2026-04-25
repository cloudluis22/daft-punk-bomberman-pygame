import pygame
import os.path
from classes.actors.bomb import Bomb
import constants

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ANIMS_FOLDER = 'assets/graphics/sprites/player'
TILE_SIZE = constants.TILE_SIZE
TM_LVL1 = constants.TM_LVL1

COLLISION_FLAGS = {
    "left": False,
    "right": False,
    "top": False,
    "bottom": False
}

def load_animations(anim_type):
    files = sorted(os.listdir(os.path.join(BASE_DIR, ANIMS_FOLDER)))
    anims_array = []

    for file in files:
        if anim_type in file:
            img = pygame.image.load(os.path.join(BASE_DIR, ANIMS_FOLDER, file)).convert_alpha()
            anims_array.append(img)

    return anims_array

def player_input(self):

    self.vx = 0
    self.vy = 0

    if self.input_handler.is_active(constants.INPUT_UP):
        self.direction = 'FW'
        self.vy = -self.speed
        self.moving = True

    if self.input_handler.is_active(constants.INPUT_DOWN):
        self.direction = 'BW'
        self.vy = self.speed
        self.moving = True

    if self.input_handler.is_active(constants.INPUT_LEFT):
        self.direction = 'LW'
        self.vx = -self.speed
        self.moving = True

    if self.input_handler.is_active(constants.INPUT_RIGHT):
        self.direction = 'RW'
        self.vx = self.speed
        self.moving = True

    if not any(action["active"] for action in self.input_handler.actions.values()):
        self.moving = False

def check_tile_collision(self):

    if not self.dead:
        # --- X movement ---
        self.rect.x += self.vx

        for rect, tile in self.rects_map:
            if self.rect.colliderect(rect):

                if self.vx > 0:
                    self.rect.right = rect.left

                if self.vx < 0:
                    self.rect.left = rect.right

        # --- Y movement ---
        self.rect.y += self.vy

        for rect, tile in self.rects_map:
            if self.rect.colliderect(rect):

                if self.vy > 0:
                    self.rect.bottom = rect.top

                if self.vy < 0:
                    self.rect.top = rect.bottom
       
def player_animation(self, FW, BW, LW, RW):

    if not self.dead:
        if self.anim_index >= 4: self.anim_index = 0

        if self.moving != True:
            match self.direction:
                case 'FW':
                    self.image = FW[1]
                case 'BW':
                    self.image = BW[1] 
                case 'LW':
                    self.image = LW[1]
                case 'RW':
                    self.image = RW[1] 
        else:
            match self.direction:
                case 'FW':
                    self.image = FW[int(self.anim_index)]
                case 'BW':
                    self.image = BW[int(self.anim_index)] 
                case 'LW':
                    self.image = LW[int(self.anim_index)]
                case 'RW':
                    self.image = RW[int(self.anim_index)]
    else:
        self.image = self.SPRT_DEAD[0]
                
#FIXME fix this
def take_damage(self):
    if not self.damage_taken:
        if self.damage_flag:
            self.damage_taken = True
            self.dead = True
            self.dead_timer = pygame.time.get_ticks()
            self.sound_manager.play_sound("sfx_player_hit")
            self.input_handler.high_freq_rumble()
            self.damage_flag = False

def death_state(self):
    if self.dead:
        now = pygame.time.get_ticks()
        if now - self.dead_timer > self.dead_duration:
            self.player_respawn()
            self.dead = False  
    
def invincible(self):
    if self.invincible:
        now = pygame.time.get_ticks()
        if now - self.invincible_timer > self.invincible_duration:
            self.invincible = False 

def bomb_spawning(self):
    if self.bomb_counter < 2:
        if self.input_handler.is_pressed(constants.INPUT_DROP_BOMB):
            tile_x = (self.rect.centerx - self.offset_x) // TILE_SIZE
            tile_y = (self.rect.centery - self.offset_y) // TILE_SIZE

            x = self.offset_x + tile_x * TILE_SIZE + TILE_SIZE // 2
            y = self.offset_y + tile_y * TILE_SIZE + TILE_SIZE // 2

            bomb = Bomb(x, y, tile_x, tile_y, TM_LVL1, self.offset_x, self.offset_y, TILE_SIZE, self.explosion_group, self.update_tilemap_def, self.sound_manager, self.input_handler)
            self.bomb_group.add(bomb)
            self.bomb_counter += 1

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, offset_x, offset_y, explosion_group, bomb_group, update_tilemap_def, rects_map, sound_manager, input_handler):
        super().__init__()
        self.ANIMS_FW = load_animations('fw')
        self.ANIMS_BW = load_animations('bw')
        self.ANIMS_LW = load_animations('lw')
        self.ANIMS_RW = load_animations('rw')
        self.SPRT_DEAD = load_animations('dead')
        self.image = self.ANIMS_BW[1]
        self.direction = 'BW'
        self.moving = False
        self.speed = 2
        self.vx = 0
        self. vy = 0
        self.anim_index = 0
        self.collision_flags = COLLISION_FLAGS
        self.bomb_counter = 0
        self.dead = False
    
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(0, -4)
        self.rect.centerx = x
        self.rect.centery = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.explosion_group = explosion_group
        self.bomb_group = bomb_group
        self.update_tilemap_def = update_tilemap_def
        self.rects_map = rects_map
        self.sound_manager = sound_manager
        self.input_handler = input_handler

        self.damage_flag = False
        self.damage_taken = False
        self.invincible = True # Invincible at spawning
        self.lives = 3
        self.invincible_timer = 0
        self.invincible_duration = 2500
        self.dead_timer = 0
        self.dead_duration = 1500
        self.spawn_x = x
        self.spawn_y = y
        
    def player_respawn(self):
        self.rect.centerx = self.spawn_x
        self.rect.centery = self.spawn_y
        self.image = self.ANIMS_BW[1]
        self.damage_taken = False
        self.invincible_timer = pygame.time.get_ticks()
        self.invincible = True

    def update(self, current_bomb_group, current_explosion_group, current_rects_map):
        check_tile_collision(self)
        self.anim_index += 0.1
        self.bomb_group = current_bomb_group
        self.explosion_group = current_explosion_group
        self.rects_map = current_rects_map
        player_input(self)
        player_animation(self, self.ANIMS_FW, self.ANIMS_BW, self.ANIMS_LW, self.ANIMS_RW)
        take_damage(self)
        bomb_spawning(self)
        invincible(self)
        death_state(self)

        if len(self.bomb_group) == 0 and len(self.explosion_group) == 0:
            self.bomb_counter = 0