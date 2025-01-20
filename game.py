import pygame
from os.path import join

from bullet import Bullet
from enemy import Enemy
from pipe import Pipe
from player import Player
from block import Block
from brick import Brick
from bonus import Bonus
from coin import Coin


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_map = []
        self.player = Player(32, 600)
        self.camera_offset = 0
        self.scroll_area_width = self.screen.get_width() // 2
        self.max_x = 0
        self.run = False
        self.theme_playing = False
        self.level = 1
        self.day_theme = pygame.mixer.Sound(join('assets', 'sounds', 'day_theme.wav'))
        self.night_theme = pygame.mixer.Sound(join('assets', 'sounds', 'night_theme.wav'))
        self.game_over_sound = pygame.mixer.Sound(join('assets', 'sounds', 'game_over.wav'))
        self.game_clear_sound = pygame.mixer.Sound(join('assets', 'sounds', 'game_clear.wav'))
        self.day_background = pygame.image.load(join("assets", "background.png")).convert()
        self.night_background = pygame.image.load(join("assets", "background_night.png")).convert()

    def generate_map(self):
        daytime = "night" if self.level == 2 else "day"

        data = []
        self.game_map = []
        with open(join("assets", "level_" + str(self.level) + ".txt")) as file:
            for line in file:
                data.append(line)

        data.reverse()
        rows = 0
        for row in data:
            rows += 1
            col_count = 0
            if row == "\n":
                continue
            for char in row:
                x = col_count * 64
                y = self.screen.get_height() - 64 * rows
                if char == "0":
                    block = Block(x, y, daytime)
                    self.game_map.append(block)
                elif char == "1":
                    brick = Brick(x, y, daytime)
                    self.game_map.append(brick)
                elif char == "2":
                    bonus = Bonus(x, y, daytime, "coin")
                    self.game_map.append(bonus)
                elif char == "3":
                    bonus = Bonus(x, y, daytime, "bullet")
                    self.game_map.append(bonus)
                elif char == "4":
                    coin = Coin(x, y)
                    self.game_map.append(coin)
                elif char == "5":
                    enemy = Enemy(x, y, daytime, "gnom", True if self.level == 2 else False)
                    self.game_map.append(enemy)
                elif char == "6":
                    enemy = Enemy(x, y, daytime, "turtle", True if self.level == 2 else False)
                    self.game_map.append(enemy)
                elif char == "7":
                    pipe = Pipe(x, y)
                    self.game_map.append(pipe)
                if x > self.max_x:
                    self.max_x = x
                col_count += 1

    def update(self):
        # Camera movement, move in direction of the player only if he is moving
        if (self.player.rect.right - self.camera_offset >= self.screen.get_width() - self.scroll_area_width and self.player.velocity > 0) or (
            self.player.rect.left - self.camera_offset <= self.scroll_area_width and self.player.velocity < 0):
            self.camera_offset += self.player.velocity

        # If the camera is supposted to go off the map, stop it from doing so.
        self.camera_offset = min(self.camera_offset, self.max_x - self.screen.get_width())
        self.camera_offset = max(self.camera_offset, 0)

        if self.level == 1:
            self.screen.blit(self.day_background, (0, 0))
            if not self.theme_playing:
                self.day_theme.play(-1)
                self.theme_playing = True
        else:
            self.screen.blit(self.night_background, (0, 0))
            if not self.theme_playing:
                self.night_theme.play(-1)
                self.theme_playing = True

        # Stop the game if the player won, or died or is off the map because of falling
        if self.player.rect.y > self.screen.get_height() + 100 or self.player.sprite_index == 4:
            self.day_theme.stop()
            self.night_theme.stop()
            if not self.player.win:
                self.game_over_sound.play()
            self.player.is_alive = False
            self.run = False
            self.theme_playing = False

        if self.player.level_clear:
            self.advance_level()

        # Update the player, enemies, render block, etc
        self.player.update(self.screen, self.game_map, self.camera_offset, self.max_x)
        for block in self.game_map:
            if abs(block.rect.x - self.player.rect.x) < self.scroll_area_width * 2:
                if type(block) is Bullet:
                    block.update(self.screen, self.camera_offset, self.game_map)
                elif type(block) is Enemy:
                    if abs(block.rect.x - self.player.rect.x) < 1280:
                        block.update(self.screen, self.camera_offset, self.game_map, self.player)
                else:
                    block.render(self.screen, self.camera_offset)

    def advance_level(self):
        self.level += 1
        if self.level > 2:
            self.game_clear_sound.play()
            self.player.win = True
            return
        if self.level == 2:
            self.day_theme.stop()
            self.theme_playing = False
        self.player.level_clear = False
        self.player.rect.x = 32
        self.player.rect.y = self.screen.get_height() - 64
        self.camera_offset = 0
        self.generate_map()

    def restart(self):
        self.day_theme.stop()
        self.night_theme.stop()
        self.level = 1
        self.run = True
        self.player.level_clear = False
        self.player.is_alive = True
        self.player.win = False
        self.theme_playing = False
        self.player.rect.x = 32
        self.player.rect.y = self.screen.get_height() - 64
        self.player.score = 0
        self.player.ammo = 0
        self.player.sprite_index = 0
        self.camera_offset = 0
        self.max_x = 0
        self.game_over_sound.stop()
        self.game_clear_sound.stop()
        self.generate_map()





