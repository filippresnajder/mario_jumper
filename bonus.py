import pygame
from os.path import join

from block import Block
from bullet import Bullet
from coin import Coin


class Bonus(Block):
    def __init__(self, x, y, daytime, bonus_type):
        super().__init__(x, y, daytime)
        self.current_sprite = 2
        self.animation_count = 0
        self.hit = False
        self.bonus_shown = False
        self.hit_time = None
        self.bonus_type = bonus_type
        self.bonus_sound_coin = pygame.mixer.Sound(join('assets', 'sounds', 'coin.wav'))
        self.bonus_sound_coin.set_volume(0.4)
        self.bonus_sound_bullet = pygame.mixer.Sound(join('assets', 'sounds', 'shoot.wav'))
        self.sound_playing = False

    def render(self, screen, camera_offset):
        if self.hit:
            if not self.bonus_shown:
                timestamp = pygame.time.get_ticks()
                self.handle_hit(self.bonus_type, screen, camera_offset)
                if timestamp - self.hit_time >= 250:
                    self.bonus_shown = True

            self.current_sprite = 0
            screen.blit(self.sprites[self.current_sprite], (self.rect.x - camera_offset, self.rect.y))
            return

        self.animate()
        screen.blit(self.sprites[self.current_sprite], (self.rect.x - camera_offset, self.rect.y))

    def animate(self):
        self.animation_count += 1
        if self.animation_count % 30 == 0:
            self.current_sprite += 1
            if self.current_sprite > 4:
                self.current_sprite = 2

    def handle_hit(self, bonus_type, screen, camera_offset):
        if bonus_type == "coin":
            coin = Coin(self.rect.x, self.rect.y-96)
            coin.render(screen, camera_offset)
            if not self.sound_playing:
                self.bonus_sound_coin.play()
                self.sound_playing = True
            return

        if bonus_type == "bullet":
            bullet = Bullet(self.rect.x, self.rect.y-96, "right", False)
            bullet.update(screen, camera_offset, None)
            if not self.sound_playing:
                self.bonus_sound_bullet.play()
                self.sound_playing = True
            return

