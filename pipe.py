import pygame
import sprites
from os.path import join


class Pipe(sprites.Sprites):
    def __init__(self, x, y):
        super().__init__(pygame.image.load(join('assets', 'blocks', 'pipe.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 128, 128)
        self.sprites = self.get_sprites(128, 128, False)

    def render(self, screen, camera_offset):
        screen.blit(self.sprites[0], (self.rect.x - camera_offset, self.rect.y))


