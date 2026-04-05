import pygame

class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(
            "assets/graphics/tiles/fire_1.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(center=(x, y))

        self.timer = 30   # frames (~0.5 sec)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            