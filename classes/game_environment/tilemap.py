import pygame as pg

def get_tile_image(tile_type, tiles_dict):
    return pg.image.load(tiles_dict[tile_type]).convert()

class Tilemap():
    
    @staticmethod            
    def create_tilemap_surface(tilemap, tile_size, tiles_dict):
        
        map_height = len(tilemap) * tile_size # Full array size.
        map_width = len(tilemap[0]) * tile_size # Size of the first row.

        map_surface = pg.Surface((map_width, map_height))

        for row_index, row in enumerate(tilemap):
            for col_index, tile_type in enumerate(row):

                tile_img = get_tile_image(tile_type, tiles_dict)
                if tile_img:
                    posX = col_index * tile_size
                    posY = row_index * tile_size
                    map_surface.blit(tile_img, (posX, posY))

        return map_surface.convert_alpha()  

    @staticmethod
    def create_rects_map(tilemap, collision_rects, tile_size, offset_x, offset_y):
        rects = []

        for row_index, row in enumerate(tilemap):
            for col_index, tile  in enumerate(row):
                if tile in collision_rects:
                    rect = pg.Rect(
                       offset_x + col_index * tile_size,
                       offset_y + row_index * tile_size,
                       tile_size,
                       tile_size 
                    )

                    rects.append((rect, tile))
        
        return rects
