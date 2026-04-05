import pygame

class H_Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, rects_map):
        super().__init__()

        self.base_image = pygame.image.load(
            "assets/graphics/sprites/enemies/enemy_2.png"
        ).convert_alpha()

        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 2
        self.direction = 1
        self.rects_map = rects_map

    def update(self, rects_map):

        self.rects_map = rects_map
        self.rect.x += self.direction * self.speed

        for rect, tile in self.rects_map:
            if self.rect.colliderect(rect):

                if self.direction > 0:
                    self.rect.right = rect.left
                else:
                    self.rect.left = rect.right

                self.direction *= -1
                break

        if self.direction < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.image = self.base_image