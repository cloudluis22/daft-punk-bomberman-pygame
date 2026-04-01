import pygame
from classes.game_environment.tilemap import Tilemap
from sys import exit
from classes.actors.player import Player
from classes.actors.bomb import Bomb
from classes.actors.venemy import VEnemy
from classes.actors.henemy import HEnemy

# VARIABLES IMPORTANTES
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

TILE_SIZE = 42
MAP_WIDTH = 15     
MAP_HEIGHT = 13
Y_OFFSET = 30

SCORE = 0

BOMB_COUNTER = 0

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

top_menu_rect = top_menu_surface.get_rect(center=(450, 50))

game_title_txt = pixel_font_lg.render('Daft Punk Bomberman', False, 'White')
game_title_rect = game_title_txt.get_rect(center=(top_menu_rect.centerx, top_menu_rect.centery - 20))

game_level_txt = pixel_font.render('Nivel 1: Rave à Paris', False, 'White')
game_level_txt_rect = game_title_txt.get_rect(center=(game_title_rect.centerx + 30, game_title_rect.bottom + 13))
 
# Fondo de pantalla de Paris para nivel 1
paris_bgrnd = pygame.image.load('assets/graphics/backgrounds/paris.png').convert()

# Esquema del NIVEL: 1 - BLOQUE INDESTRUCTIBLE/MURO 2 - BLOQUE DESTRUCTIBLE 3 - BLOQUE CAMINABLE
TILEMAP = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 3, 1],
[1, 2, 1, 0, 1, 0, 1, 2, 1, 2, 1, 2, 1, 0, 1],
[1, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 1],
[1, 2, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1],
[1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1],
[1, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
[1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1],
[1, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 0, 0, 1],
[1, 0, 1, 2, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

tiles = {
    0: pygame.image.load('assets/graphics/tiles/concrete_floor.png').convert(),
    1: pygame.image.load('assets/graphics/tiles/concrete_wall.png').convert(),
    2: pygame.image.load('assets/graphics/tiles/crate.png').convert(),
    3: pygame.image.load('assets/graphics/tiles/spawn.png').convert()
}
 
map_pixel_width = MAP_WIDTH * TILE_SIZE
map_pixel_height = MAP_HEIGHT * TILE_SIZE

offset_x = (SCREEN_WIDTH - map_pixel_width) // 2
offset_y = (SCREEN_HEIGHT - map_pixel_height) // 2 + Y_OFFSET

def draw_map(screen, tilemap, tiles, offset_x=0, offset_y=0):
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):            
            screen.blit(
                tiles[tile],
                (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE)
            )

def create_tile_rects(tilemap, collision_tiles, offset_x=0, offset_y=0):
    rects = []

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):

            if tile in collision_tiles:
                rect = pygame.Rect(
                    offset_x + x * TILE_SIZE,
                    offset_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                rects.append((rect, tile))

    return rects

def find_spawn_point(tilemap):
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 3:
                return pygame.Rect(
                    offset_x + x * TILE_SIZE,
                    offset_y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE)
            
spawn_point = find_spawn_point(TILEMAP)
player = Player(spawn_point.centerx, spawn_point.centery)
player_group.add(player)
explosion_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

game_lives_c_txt = pixel_font.render(f'X{player.lives}', False, 'White')
game_lives_c_txt_rect = game_lives_c_txt.get_rect(center=(top_menu_rect.left + 80, top_menu_rect.centery - 10))
thomas_lives_icon_rect = thomas_lives_icon.get_rect(center=(top_menu_rect.left + 48, top_menu_rect.centery - 12))

game_score_txt = pixel_font.render(f'PUNTUACIÓN: {SCORE}', False, 'White')
game_score_txt_rect = game_score_txt.get_rect(center=(top_menu_rect.left + 100, top_menu_rect.centery + 13))

# rects_map = create_tile_rects(TILEMAP, [1, 2], offset_x, offset_y)\
rects_map = Tilemap.create_rects_map(TILEMAP, [1, 2], TILE_SIZE, offset_x, offset_y)
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
 
def bomb_spawning(bomb_counter):

    if bomb_counter < 2:
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:

            tile_x = (player.rect.centerx - offset_x) // TILE_SIZE
            tile_y = (player.rect.centery - offset_y) // TILE_SIZE

            x = offset_x + tile_x * TILE_SIZE + TILE_SIZE // 2
            y = offset_y + tile_y * TILE_SIZE + TILE_SIZE // 2

            bomb = Bomb(x, y, tile_x, tile_y, TILEMAP, offset_x, offset_y, TILE_SIZE, explosion_group)
            bomb_group.add(bomb)
            bomb_counter += 1
    return bomb_counter

def flash_player():
    if player.invincible:
        if pygame.time.get_ticks() % 50 < 10:
            return
    player_group.draw(screen)

map_surface = Tilemap.create_tilemap_surface(TILEMAP, TILE_SIZE, tiles)

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
    BOMB_COUNTER = bomb_spawning(BOMB_COUNTER)
    player_group.update()
    bomb_group.draw(screen)
    bomb_group.update()
    explosion_group.update()
    explosion_group.draw(screen)
    # rects_map = create_tile_rects(TILEMAP, [1, 2], offset_x, offset_y)
    rects_map = Tilemap.create_rects_map(TILEMAP, [1, 2], TILE_SIZE, offset_x, offset_y)
    enemies_group.draw(screen)
    enemies_group.update(rects_map)
    flash_player()

    for explosion in explosion_group:
        if(player.rect.colliderect(explosion)):
            player.damage_flag = True
       
    for enemy in enemies_group:
        if(player.rect.colliderect(enemy)):
            player.damage_flag = True

    if len(bomb_group) == 0 and len(explosion_group) == 0:
        BOMB_COUNTER = 0

    enemy_deaths = pygame.sprite.groupcollide(enemies_group, explosion_group, True, False)
    if enemy_deaths:
        enemy_hit.play()
        SCORE += 200

    pygame.display.update()
    clock.tick(60)