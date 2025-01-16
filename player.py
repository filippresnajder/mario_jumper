import pygame
import sprites
from os.path import join

from bonus import Bonus
from bullet import Bullet
from coin import Coin
from enemy import Enemy
from pipe import Pipe

PLAYER_VELOCITY = 8
PLAYER_GRAVITY = 2
PLAYER_JUMP = 35
SHOOT_COOLDOWN = 500
KEY_COOLDOWN = 2000


class Player(sprites.Sprites):
    def __init__(self, x, y):
        super().__init__(pygame.image.load(join('assets', 'mario', 'mario.png')).convert_alpha())
        self.rect = pygame.Rect(x, y, 64, 64)
        self.velocity = 0
        self.gravity = 0
        self.sprites = self.get_sprites(64, 64, True)
        self.direction = "right"
        self.animation_count = 0
        self.sprite_index = 0
        self.score = 0
        self.ammo = 0
        self.shooting_cooldown = 0
        self.key_cooldown = 0
        self.is_on_pipe = False
        self.is_jumping = False
        self.level_clear = False
        self.win = False
        self.is_alive = False
        self.jump_sound = pygame.mixer.Sound(join('assets', 'sounds', 'jump.wav'))
        self.jump_sound.set_volume(0.4)
        self.bullet_shot_sound = pygame.mixer.Sound(join('assets', 'sounds', 'shoot.wav'))
        self.coin_sound = pygame.mixer.Sound(join('assets', 'sounds', 'coin.wav'))
        self.coin_sound.set_volume(0.4)

    def move_left(self, dx, game_map):
        self.rect.x -= dx
        if self.rect.left < 0:
            self.rect.left = 0
            return
        if self.direction != "left":
            self.direction = "left"
        self.velocity = -dx
        self.check_horizontal_collision(game_map)

    def move_right(self, dx, game_map, max_x):
        self.rect.x += dx
        if self.rect.right > max_x:
            self.rect.right = max_x
            return
        if self.direction != "right":
            self.direction = "right"
        self.velocity = dx
        self.check_horizontal_collision(game_map)

    def jump(self, dy):
        if not self.is_jumping:
            self.is_jumping = True
            self.gravity = -dy
            self.rect.y -= dy
            self.jump_sound.play()

    def apply_gravity(self, game_map):
        self.gravity += PLAYER_GRAVITY
        self.rect.y += self.gravity
        self.check_vertical_collision(game_map)

    def shoot(self, game_map):
        self.shooting_cooldown = pygame.time.get_ticks()
        bullet = Bullet(self.rect.x, self.rect.y, self.direction, True)
        game_map.append(bullet)
        self.ammo -= 1
        self.bullet_shot_sound.play()

    def handle_move(self, game_map, max_x):
        key = pygame.key.get_pressed()
        self.velocity = 0
        if key[pygame.K_a]:
            self.move_left(PLAYER_VELOCITY + (4 if key[pygame.K_SPACE] else 1), game_map)
        if key[pygame.K_d]:
            self.move_right(PLAYER_VELOCITY + (4 if key[pygame.K_SPACE] else 1), game_map, max_x)
        if key[pygame.K_w]:
            self.jump(PLAYER_JUMP)
        if key[pygame.K_s] and self.is_on_pipe and self.key_cooldown == 0:
            self.key_cooldown = pygame.time.get_ticks()
            self.level_clear = True
        if key[pygame.K_q] and self.shooting_cooldown == 0 and self.ammo > 0:
            self.shoot(game_map)

    def animate_sprite(self):
        # If sprite index is 4 it means that the player has died and the game is over
        if self.sprite_index == 4:
            return
        # If player is currently jumping force the sprite to be on the 3rd index
        if self.is_jumping:
            self.animation_count = 0
            self.sprite_index = 3
            return
        # Handle situation when the player is idle
        if self.velocity == 0:
            self.animation_count = 0
            self.sprite_index = 0
            return
        self.animation_count += 1
        if self.animation_count % 5 == 0:
            self.sprite_index += 1
            if self.sprite_index > 2:
                self.sprite_index = 0

    def check_vertical_collision(self, game_map):
        if not self.is_alive:
            return
        self.is_on_pipe = False
        for block in game_map:
            if self.rect.colliderect(block.rect):
                if type(block) not in [Coin, Bullet]:
                    # Is Falling
                    if self.gravity > 0:
                        if type(block) is Enemy and block.alive:
                            if block.agressive:
                                self.is_alive = False
                            else:
                                block.alive = False
                                block.death_timestamp = pygame.time.get_ticks()
                                self.rect.bottom = block.rect.bottom
                        if type(block) is not Enemy:
                            self.rect.bottom = block.rect.top
                        if type(block) is Pipe:
                            self.is_on_pipe = True
                        self.gravity = 0
                        self.is_jumping = False
                    # Is Jumping
                    elif self.gravity < 0:
                        self.rect.top = block.rect.bottom
                        self.gravity = 0
                        if type(block) is Bonus and not block.hit:
                            block.hit_time = pygame.time.get_ticks()
                            block.hit = True
                            if block.bonus_type == "bullet":
                                self.ammo += 1
                            self.score += 100
                elif type(block) is Coin:
                    game_map.remove(block)
                    self.score += 100
                    self.coin_sound.play()

    def check_horizontal_collision(self, game_map):
        if not self.is_alive:
            return
        for block in game_map:
            if self.rect.colliderect(block.rect):
                if type(block) not in [Bullet, Coin, Enemy]:
                    # Moving Right
                    if self.velocity > 0:
                        self.rect.right = block.rect.left
                    # Moving Left
                    elif self.velocity < 0:
                        self.rect.left = block.rect.right
                    self.velocity = 0
                elif type(block) is Coin:
                    game_map.remove(block)
                    self.score += 100
                    self.coin_sound.play()
                elif type(block) is Enemy and block.alive:
                    self.is_alive = False

    def update(self, screen, game_map, camera_offset, max_x):
        # If the player had won, set its sprite to 4
        if not self.is_alive or self.win:
            self.sprite_index = 4
            screen.blit(self.sprites[self.direction][self.sprite_index], (self.rect.x - camera_offset, self.rect.y))
            return
        timestamp = pygame.time.get_ticks()
        self.handle_move(game_map, max_x)
        self.animate_sprite()
        self.apply_gravity(game_map)
        if timestamp - self.shooting_cooldown >= SHOOT_COOLDOWN:
            self.shooting_cooldown = 0
        if timestamp - self.key_cooldown >= KEY_COOLDOWN:
            self.key_cooldown = 0
        screen.blit(self.sprites[self.direction][self.sprite_index], (self.rect.x - camera_offset, self.rect.y))


