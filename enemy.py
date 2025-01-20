import pygame
import sprites
from os.path import join

from block import Block

ENEMY_SPEED = 4
ENEMY_GRAVITY = 2


class Enemy(sprites.Sprites):
    def __init__(self, x, y, daytime, enemy_type, aggression):
        super().__init__(pygame.image.load(join('assets', 'enemies', daytime, enemy_type + '.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 64, 64)
        self.sprites = self.get_sprites(64, 64, True)
        self.current_sprite = 0
        self.animation_count = 0
        self.gravity = 0
        self.direction = "left"
        self.alive = True
        self.given_score = False
        self.movement_started = False
        self.death_timestamp = 0
        self.death_sound = pygame.mixer.Sound(join('assets', 'sounds', 'enemy_death.wav'))
        self.death_sound_played = False
        self.agressive = aggression

    def move(self, screen, game_map, player):
        self.rect.x += (ENEMY_SPEED if self.direction == "right" else -ENEMY_SPEED) * (1.5 if self.agressive else 1)
        self.gravity += ENEMY_GRAVITY
        self.rect.y += self.gravity
        self.check_vertical_collision(game_map, player)
        self.check_horizontal_collision(game_map, player)

        # If the enemy has fallen off the map, remove it
        if self.rect.y > screen.get_height() + 100:
            game_map.remove(self)

    def animate_sprite(self):
        self.animation_count += 1
        if self.animation_count % 20 == 0:
            self.current_sprite += 1
            if self.current_sprite > 1:
                self.current_sprite = 0

    def check_vertical_collision(self, game_map, player):
        for block in game_map:
            if self.rect.colliderect(block.rect) and isinstance(block, Block):
                self.gravity = 0
                self.rect.bottom = block.rect.top
                break

    def check_horizontal_collision(self, game_map, player):
        for block in game_map:
            if self.rect.colliderect(player.rect) and self.alive:
                player.is_alive = False
                break

            if self.rect.colliderect(block.rect) and isinstance(block, Block):
                if self.direction == "left":
                    self.direction = "right"
                    self.rect.left = block.rect.right
                else:
                    self.direction = "left"
                    self.rect.right = block.rect.left
                break

    def update(self, screen, camera_offset, game_map, player):
        if not self.alive:

            if not self.death_sound_played:
                self.death_sound.play()
                self.death_sound_played = True

            self.current_sprite = 2
            screen.blit(self.sprites[self.direction][self.current_sprite], (self.rect.x - camera_offset, self.rect.y))

            if not self.given_score:
                player.score += 100
                self.given_score = True

            if pygame.time.get_ticks() - self.death_timestamp > 300:
                game_map.remove(self)

            return

        self.move(screen, game_map, player)
        self.animate_sprite()
        screen.blit(self.sprites[self.direction][self.current_sprite], (self.rect.x - camera_offset, self.rect.y))

