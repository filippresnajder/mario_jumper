import pygame
import sprites
from os.path import join

from block import Block
from enemy import Enemy
from pipe import Pipe

BULLET_SPEED = 8


class Bullet(sprites.Sprites):
    def __init__(self, x, y, direction, shot):
        super().__init__(pygame.image.load(join('assets', 'mario', 'bullet.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 64, 64)
        self.sprites = self.get_sprites(64, 64, True)
        self.direction = direction
        self.shot = shot
        self.hit = False

    def update(self, screen, camera_offset, game_map):
        if self.hit:
            return
        if not self.shot:
            screen.blit(self.sprites[self.direction][0], (self.rect.x - camera_offset, self.rect.y))
            return
        self.rect.x += BULLET_SPEED if self.direction == "right" else -BULLET_SPEED
        self.check_collision(game_map)
        screen.blit(self.sprites[self.direction][0], (self.rect.x - camera_offset, self.rect.y))

    def check_collision(self, game_map):
        for block in game_map:
            if self.rect.colliderect(block.rect):
                if isinstance(block, Block) or isinstance(block, Pipe):
                    self.hit = True
                elif isinstance(block, Enemy) and block.alive:
                    self.hit = True
                    block.alive = False
                    block.death_timestamp = pygame.time.get_ticks()


