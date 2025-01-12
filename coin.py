import pygame
import sprites
from os.path import join


class Coin(sprites.Sprites):
    def __init__(self, x, y):
        super().__init__(pygame.image.load(join('assets', 'blocks', 'coins.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 64, 64)
        self.sprites = self.get_sprites(64, 64, False)
        self.current_sprite = 0
        self.animation_count = 0

    def render(self, screen, camera_offset):
        self.animate()
        screen.blit(self.sprites[self.current_sprite], (self.rect.x - camera_offset, self.rect.y))

    def animate(self):
        self.animation_count += 1
        if self.animation_count % 20 == 0:
            self.current_sprite += 1
            if self.current_sprite > 2:
                self.current_sprite = 0
