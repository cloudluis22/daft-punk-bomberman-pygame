import pygame as pg
import constants
from pathlib import Path
from classes.game_environment.tilemap import Tilemap
from classes.actors.player import Player
from classes.actors.v_enemy import V_Enemy
from classes.actors.h_enemy import H_Enemy
from classes.interface.hud import HUD

current_path = Path(__file__).parent
root_path = current_path.parent.parent

paris_bg = root_path / "assets" / "graphics" / "backgrounds" / "paris.png"

class LevelManager():
    def __init__(self, screen, sound_manager, input_handler):

        # SCREEN 
        self.screen = screen

        # MANAGERS
        self.sound_manager = sound_manager

        # INPUT HANDLER
        self.input_handler = input_handler

        # TILEMAP RELATED VARIABLES
        self.rects_map = []
        self.map_surface = None
        self.map_pixel_width = constants.TM_WIDTH * constants.TILE_SIZE
        self.map_pixel_height = constants.TM_HEIGHT * constants.TILE_SIZE
        self.current_bg = ""

        self.current_tilemap = []
        self.collision_tiles = []
        self.current_tiles = []
        
        self.offset_x = (constants.SCREEN_WIDTH - self.map_pixel_width) // 2
        self.offset_y = (constants.SCREEN_HEIGHT - self.map_pixel_height) // 2 + constants.TM_Y_OFFSET

        # SPRITE GROUPS.
        self.player_group = pg.sprite.GroupSingle()
        self.bomb_group = pg.sprite.Group()
        self.enemies_group = pg.sprite.Group()
        self.explosion_group = pg.sprite.Group()
        self.hud_group = pg.sprite.GroupSingle()        

        # GAME RELATED VARIABLES
        self.score = 0
        self.time = 60
        self.game_over = False

    def spawn_entities(self):
        for row_index, row in enumerate(self.current_tilemap):
            for col_index, tile in enumerate(row):
                point = pg.Rect(
                    self.offset_x + col_index * constants.TILE_SIZE,
                    self.offset_y + row_index * constants.TILE_SIZE,
                    constants.TILE_SIZE,
                    constants.TILE_SIZE)
                if tile == 3:
                    player = Player(point.centerx,
                                    point.centery,
                                    self.offset_x,
                                    self.offset_y,
                                    self.explosion_group,
                                    self.bomb_group,
                                    self.update_tilemap,
                                    self.rects_map,
                                    self.sound_manager,
                                    self.input_handler)
                    self.player_group.add(player)
                elif tile == 5:
                    v_enemy = V_Enemy(point.centerx, point.centery, self.rects_map)
                    self.enemies_group.add(v_enemy)
                elif tile == 6:
                    h_enemy = H_Enemy(point.centerx, point.centery, self.rects_map)
                    self.enemies_group.add(h_enemy)

    def update_tilemap(self, x, y):
        self.rects_map = Tilemap.update_rects_map(self.rects_map, x, y, self.offset_x, self.offset_y, constants.TILE_SIZE)
        Tilemap.update_map_surface(self.map_surface, x, y, 0, self.current_tiles, constants.TILE_SIZE)

    def flash_player(self):
        player = self.player_group.sprites()[0]
        if player.invincible:
            if pg.time.get_ticks() % 30 < 10:
                return
        self.player_group.draw(self.screen)

    def load_level(self, level):

        match level:
            case 1:
                self.current_tilemap = constants.TM_LVL1
                self.collision_tiles = [1, 2]
                self.current_tiles = {k: pg.image.load(v).convert() for k, v in constants.TILES_LVL1.items()}
                self.current_bg = pg.image.load(paris_bg)

        self.rects_map = Tilemap.create_rects_map(self.current_tilemap,
                                            self.collision_tiles,
                                            constants.TILE_SIZE,
                                            self.offset_x, self.offset_y)
        
        self.map_surface = Tilemap.create_tilemap_surface(self.current_tilemap, constants.TILE_SIZE, self.current_tiles)

        event_loaded = pg.event.Event(constants.EV_MAP_LOADED)
        pg.event.post(event_loaded)

    def unload_level(self):
        self.current_tilemap = []
        self.collision_tiles = []
        self.current_tiles = []
        self.rects_map = []
        self.map_surface = None
        self.current_bg = ""
        self.player_group.empty()
        self.enemies_group.empty()
        self.explosion_group.empty()

    def level_start(self, level):
        self.spawn_entities()
        player = self.player_group.sprites()[0]
        hud = HUD(self.screen, player, self.score, player.lives, self.time)
        self.hud_group.add(hud)
        evt_level_run = pg.event.Event(constants.EV_LEVEL_RUN)
        pg.time.set_timer(constants.EV_LEVEL_TIME_PASSING, 1000)
        pg.event.post(evt_level_run)

        match level:
            case 1:
                self.sound_manager.play_music("mus_level1")

    def update_level(self):

        if self.time <= 0:
            self.time = 0

        player = self.player_group.sprites()[0]

        if player.lives <= 0 or self.time <= 0:
            self.game_over = True

        if self.game_over:
            print("GAME OVER YEAHH")

        self.screen.blit(self.current_bg, (0, 0))
        self.screen.blit(self.map_surface, (self.offset_x, self.offset_y))
        self.player_group.update(self.bomb_group, self.explosion_group, self.rects_map)
        self.bomb_group.draw(self.screen)
        self.bomb_group.update()
        self.explosion_group.update()
        self.explosion_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.enemies_group.update(self.rects_map)
        self.hud_group.update(player.lives, self.score, self.time)
        self.hud_group.draw(self.screen)
        self.flash_player()
    
        for explosion in self.explosion_group:
            if(player.rect.colliderect(explosion)):
                if not player.invincible:
                    player.damage_flag = True

            for bomb in self.bomb_group:
                if explosion.rect.colliderect(bomb):
                    bomb.explode()
                    bomb.kill()
        
        for enemy in self.enemies_group:
            if(player.rect.colliderect(enemy)):
                if not player.invincible:
                    player.damage_flag = True
                    enemy.collision(player.rect)
            
            for bomb in self.bomb_group:
                if bomb.rect.colliderect(enemy):
                    enemy.collision(bomb.rect)
        
        enemy_deaths = pg.sprite.groupcollide(self.enemies_group, self.explosion_group, True, False)
        if enemy_deaths:
            self.sound_manager.play_sound("sfx_enemy_hit")
            self.score += 200