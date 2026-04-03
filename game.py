import pygame
import constants
from sys import exit
from classes.game_environment.tilemap import Tilemap
from classes.actors.player import Player
from classes.actors.venemy import VEnemy
from classes.actors.henemy import HEnemy

# IMPORTANT VARIABLES
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

TILE_SIZE = constants.TILE_SIZE
MAP_WIDTH = constants.TM_WIDTH     
MAP_HEIGHT = constants.TM_HEIGHT
MAP_Y_OFFSET = constants.TM_Y_OFFSET

SCORE = 0

LVL1_TM = constants.TM_LVL1

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Daft Bomberman")
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("assets/sound/music/music1.mp3")
pygame.mixer.music.set_volume(0.6)
player_group = pygame.sprite.GroupSingle()
bomb_group = pygame.sprite.Group()

pygame.mixer.music.play(-1)  # -1 = loop forever
enemy_hit = pygame.mixer.Sound('assets/sound/sfx/enemy_hit.mp3')
enemy_hit.set_volume(0.7)

player_hit = pygame.mixer.Sound('assets/sound/sfx/hurt.mp3')
player_hit.set_volume(0.7)

pixel_font_lg = pygame.font.Font('assets/fonts/pixel_font.ttf', 30)
pixel_font = pygame.font.Font('assets/fonts/pixel_font.ttf', 25)

thomas_lives_icon = pygame.image.load('assets/graphics/icons/thomas_icon.png').convert_alpha()

top_menu_surface = pygame.Surface((830, 75), pygame.SRCALPHA)

pygame.draw.rect(
    top_menu_surface,
    (176, 176, 176, 200), 
    (0, 0, 830, 75),        
)

TILES_LV1 = {k: pygame.image.load(v).convert() for k, v in constants.TILES_LVL1.items()}

top_menu_rect = top_menu_surface.get_rect(center=(450, 50))

game_title_txt = pixel_font_lg.render('Daft Punk Bomberman', False, 'White')
game_title_rect = game_title_txt.get_rect(center=(top_menu_rect.centerx, top_menu_rect.centery - 20))

game_level_txt = pixel_font.render('Nivel 1: Rave à Paris', False, 'White')
game_level_txt_rect = game_title_txt.get_rect(center=(game_title_rect.centerx + 30, game_title_rect.bottom + 13))
 
# Fondo de pantalla de Paris para nivel 1
paris_bgrnd = pygame.image.load('assets/graphics/backgrounds/paris.png').convert()
 
map_pixel_width = MAP_WIDTH * TILE_SIZE
map_pixel_height = MAP_HEIGHT * TILE_SIZE

offset_x = (SCREEN_WIDTH - map_pixel_width) // 2
offset_y = (SCREEN_HEIGHT - map_pixel_height) // 2 + MAP_Y_OFFSET
rects_map = Tilemap.create_rects_map(LVL1_TM, [1, 2], TILE_SIZE, offset_x, offset_y)
map_surface = Tilemap.create_tilemap_surface(LVL1_TM, TILE_SIZE, TILES_LV1)

def find_spawn_point(tilemap):
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 3:
                return pygame.Rect(
                    offset_x + x * TILE_SIZE,
                    offset_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE)
            
def update_tilemap(x, y):
    global rects_map
    global map_surface

    rects_map = Tilemap.update_rects_map(rects_map, x, y, offset_x, offset_y, TILE_SIZE)
    Tilemap.update_map_surface(map_surface, x, y, 0, TILES_LV1, TILE_SIZE)

spawn_point = find_spawn_point(LVL1_TM)
explosion_group = pygame.sprite.Group()
player = Player(spawn_point.centerx, spawn_point.centery, offset_x, offset_y, explosion_group, bomb_group, update_tilemap)
player_group.add(player)
enemies_group = pygame.sprite.Group()

game_lives_c_txt = pixel_font.render(f'X{player.lives}', False, 'White')
game_lives_c_txt_rect = game_lives_c_txt.get_rect(center=(top_menu_rect.left + 80, top_menu_rect.centery - 10))
thomas_lives_icon_rect = thomas_lives_icon.get_rect(center=(top_menu_rect.left + 48, top_menu_rect.centery - 12))

game_score_txt = pixel_font.render(f'PUNTUACIÓN: {SCORE}', False, 'White')
game_score_txt_rect = game_score_txt.get_rect(center=(top_menu_rect.left + 100, top_menu_rect.centery + 13))


enemies_group.add(VEnemy(365,200, rects_map))
enemies_group.add(VEnemy(447,581, rects_map))
enemies_group.add(VEnemy(281,297, rects_map))
enemies_group.add(VEnemy(448,252, rects_map))
enemies_group.add(VEnemy(533,333, rects_map))
enemies_group.add(HEnemy(195,586, rects_map))
enemies_group.add(HEnemy(533,254, rects_map))
enemies_group.add(HEnemy(322,421, rects_map))
enemies_group.add(HEnemy(576,423, rects_map))
enemies_group.add(HEnemy(197,253, rects_map))
enemies_group.add(HEnemy(448,170, rects_map))
enemies_group.add(HEnemy(531,590, rects_map))

def check_tile_collision(player, rects_map):

    # --- X movement ---
    player.rect.x += player.vx

    for rect, tile in rects_map:
        if player.rect.colliderect(rect):

            if player.vx > 0:
                player.rect.right = rect.left

            if player.vx < 0:
                player.rect.left = rect.right

    # --- Y movement ---
    player.rect.y += player.vy

    for rect, tile in rects_map:
        if player.rect.colliderect(rect):

            if player.vy > 0:
                player.rect.bottom = rect.top

            if player.vy < 0:
                player.rect.top = rect.bottom
 
def flash_player():
    if player.invincible:
        if pygame.time.get_ticks() % 50 < 10:
            return
    player_group.draw(screen)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game_lives_c_txt = pixel_font.render(f'X{player.lives}', False, 'White')
    game_score_txt = pixel_font.render(f'PUNTUACIÓN: {SCORE}', False, 'White')
    screen.blit(paris_bgrnd, (0, 0))
    screen.blit(map_surface, (offset_x, offset_y))
    screen.blit(top_menu_surface, top_menu_rect)
    screen.blit(game_title_txt, game_title_rect)
    screen.blit(game_level_txt, game_level_txt_rect)
    screen.blit(game_lives_c_txt, game_lives_c_txt_rect)
    screen.blit(thomas_lives_icon, thomas_lives_icon_rect)
    screen.blit(game_score_txt, game_score_txt_rect)
    check_tile_collision(player, rects_map)
    player_group.update(bomb_group, explosion_group)
    bomb_group.draw(screen)
    bomb_group.update()
    explosion_group.update()
    explosion_group.draw(screen)
    enemies_group.draw(screen)
    enemies_group.update(rects_map)
    flash_player()

    for explosion in explosion_group:
        if(player.rect.colliderect(explosion)):
            player.damage_flag = True
       
    for enemy in enemies_group:
        if(player.rect.colliderect(enemy)):
            player.damage_flag = True

    enemy_deaths = pygame.sprite.groupcollide(enemies_group, explosion_group, True, False)
    if enemy_deaths:
        enemy_hit.play()
        SCORE += 200

    pygame.display.update()
    clock.tick(60)