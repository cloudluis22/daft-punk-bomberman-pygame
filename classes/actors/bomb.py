import pygame
from classes.actors.explosion import Explosion

def get_explosion_tiles(tilemap, bomb_x, bomb_y, radius=1):

    affected = [(bomb_x, bomb_y)]  # center tile (bomb itself)

    directions = [
        (1, 0),   # right
        (-1, 0),  # left
        (0, 1),   # down
        (0, -1)   # up
    ]

    for dx, dy in directions:
        for i in range(1, radius + 1):

            x = bomb_x + dx * i
            y = bomb_y + dy * i

            tile = tilemap[y][x]

            # stop if wall
            if tile == 1:
                break

            affected.append((x, y))

            # stop after destroying crate
            if tile == 2:
                break

    return affected

class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y, tile_x, tile_y, tilemap, offset_x, offset_y, tile_size, explosion_group, update_tm):
        super().__init__()

        self.image = pygame.image.load("assets/graphics/sprites/bomb/bomb_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.timer = 180

        self.tilemap = tilemap
        
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.tile_size = tile_size

        self.explosion_group = explosion_group

        self.explosion_sfx = pygame.mixer.Sound('assets/sound/sfx/explosion.mp3')
        self.explosion_sfx.set_volume(0.8)

        self.update_tm = update_tm

    def update(self):

        self.timer -= 1

        if self.timer <= 0:
            self.explode()
            self.explosion_sfx.play()
            self.kill()

    def explode(self):

        affected_tiles = get_explosion_tiles(self.tilemap, self.tile_x, self.tile_y, 2)

        for x, y in affected_tiles:

            px = self.offset_x + x * self.tile_size + self.tile_size // 2
            py = self.offset_y + y * self.tile_size + self.tile_size // 2

            explosion = Explosion(px, py)
            self.explosion_group.add(explosion)

            if self.tilemap[y][x] == 2:
                self.tilemap[y][x] = 0
            
            self.update_tm()