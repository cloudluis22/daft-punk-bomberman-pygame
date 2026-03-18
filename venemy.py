import pygame

class VEnemy(pygame.sprite.Sprite):

    def __init__(self, x, y, rects_map):
        super().__init__()

        self.images = [
            pygame.image.load("assets/graphics/sprites/enemies/enemy_1b.png").convert_alpha(),
            pygame.image.load("assets/graphics/sprites/enemies/enemy_1a.png").convert_alpha()
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 2
        self.direction = -1   # -1 = up, 1 = down
        self.rects_map = rects_map

    def update(self, rects_map):

        self.rects_map = rects_map
        self.rect.y += self.direction * self.speed

        for rect, tile in self.rects_map:
            if self.rect.colliderect(rect):

                if self.direction > 0:
                    self.rect.bottom = rect.top
                else:
                    self.rect.top = rect.bottom

                self.direction *= -1
                break

        if self.direction < 0:
            self.image = self.images[0]
        else:
            self.image = self.images[1]