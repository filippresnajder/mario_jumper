import pygame
import sprites
from os.path import join


class Block(sprites.Sprites):
    def __init__(self, x, y, daytime):
        super().__init__(pygame.image.load(join('assets', 'blocks', daytime, 'blocks.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 64, 64)
        self.sprites = self.get_sprites(64, 64, False)

    def render(self, screen, camera_offset):
        screen.blit(self.sprites[5], (self.rect.x - camera_offset, self.rect.y))


