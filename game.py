import pygame
import constants
from sys import exit
from classes.interface.hud import HUD
from classes.game_environment.tilemap import Tilemap
from classes.actors.player import Player
from classes.actors.v_enemy import V_Enemy
from classes.actors.h_enemy import H_Enemy

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
enemies_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
hud_group = pygame.sprite.GroupSingle()

TILES_LV1 = {k: pygame.image.load(v).convert() for k, v in constants.TILES_LVL1.items()}

pygame.mixer.music.play(-1)  # -1 = loop forever
enemy_hit = pygame.mixer.Sound('assets/sound/sfx/enemy_hit.mp3')
enemy_hit.set_volume(0.7)

player_hit = pygame.mixer.Sound('assets/sound/sfx/hurt.mp3')
player_hit.set_volume(0.7)

# Fondo de pantalla de Paris para nivel 1
paris_bgrnd = pygame.image.load('assets/graphics/backgrounds/paris.png').convert()
 
map_pixel_width = MAP_WIDTH * TILE_SIZE
map_pixel_height = MAP_HEIGHT * TILE_SIZE

offset_x = (SCREEN_WIDTH - map_pixel_width) // 2
offset_y = (SCREEN_HEIGHT - map_pixel_height) // 2 + MAP_Y_OFFSET
rects_map = Tilemap.create_rects_map(LVL1_TM, [1, 2], TILE_SIZE, offset_x, offset_y)
map_surface = Tilemap.create_tilemap_surface(LVL1_TM, TILE_SIZE, TILES_LV1)

def update_tilemap(x, y):
    global rects_map
    global map_surface

    rects_map = Tilemap.update_rects_map(rects_map, x, y, offset_x, offset_y, TILE_SIZE)
    Tilemap.update_map_surface(map_surface, x, y, 0, TILES_LV1, TILE_SIZE)

def spawn_entities(tilemap):
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            point = pygame.Rect(
                offset_x + col_index * TILE_SIZE,
                offset_y + row_index * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE)
            if tile == 3:
                player = Player(point.centerx, point.centery, offset_x, offset_y, explosion_group, bomb_group, update_tilemap, rects_map)
                player_group.add(player)
            elif tile == 5:
                v_enemy = V_Enemy(point.centerx, point.centery, rects_map)
                enemies_group.add(v_enemy)
            elif tile == 6:
                h_enemy = H_Enemy(point.centerx, point.centery, rects_map)
                enemies_group.add(h_enemy)

spawn_entities(LVL1_TM)
player = player_group.sprites()[0]
hud = HUD(screen, player, SCORE, player.lives)
hud_group.add(hud)

def flash_player():
    if player.invincible:
        if pygame.time.get_ticks() % 30 < 10:
            return
    player_group.draw(screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(paris_bgrnd, (0, 0))
    screen.blit(map_surface, (offset_x, offset_y))
    player_group.update(bomb_group, explosion_group, rects_map)
    bomb_group.draw(screen)
    bomb_group.update()
    explosion_group.update()
    explosion_group.draw(screen)
    enemies_group.draw(screen)
    enemies_group.update(rects_map)
    hud_group.update(player.lives, SCORE)
    hud_group.draw(screen)
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