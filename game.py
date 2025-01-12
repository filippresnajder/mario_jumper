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
        self.bg = pygame.transform.scale(pygame.image.load(join("assets", "background.png")), (screen.get_width(), screen.get_height()))
        self.game_map = []
        self.player = Player(32, self.screen.get_height()-64)
        self.camera_offset = 0
        self.scroll_area_width = (self.screen.get_width() // 2)
        self.max_x = 0
        self.run = False
        self.level = 1
        self.day_theme = pygame.mixer.Sound(join('assets', 'sounds', 'day_theme.wav'))
        self.night_theme = pygame.mixer.Sound(join('assets', 'sounds', 'night_theme.wav'))
        self.game_over_sound = pygame.mixer.Sound(join('assets', 'sounds', 'game_over.wav'))
        self.game_clear_sound = pygame.mixer.Sound(join('assets', 'sounds', 'game_clear.wav'))

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
                    enemy = Enemy(x, y, daytime, "gnom")
                    self.game_map.append(enemy)
                elif char == "6":
                    enemy = Enemy(x, y, daytime, "turtle")
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

        self.screen.blit(self.bg, (0, 0))

        # Update the player, enemies, render block, etc
        self.player.update(self.screen, self.game_map, self.camera_offset, self.max_x)
        for block in self.game_map:
            if type(block) is Bullet:
                block.update(self.screen, self.camera_offset, self.game_map)
            elif type(block) is Enemy:
                block.update(self.screen, self.camera_offset, self.game_map, self.player)
            else:
                block.render(self.screen, self.camera_offset)

        # Stop the game if the player won, or died or is off the map because of falling
        if self.player.rect.y > self.screen.get_height() + 100 or self.player.sprite_index == 4:
            self.day_theme.stop()
            self.night_theme.stop()
            if not self.player.win:
                self.game_over_sound.play()
            self.player.is_alive = False
            self.run = False

        if self.player.level_clear:
            self.advance_level()

    def advance_level(self):
        self.level += 1
        if self.level > 2:
            self.game_clear_sound.play()
            self.player.win = True
            return
        if self.level == 2:
            self.bg = pygame.transform.scale(pygame.image.load(join("assets", "background_night.png")), (self.screen.get_width(), self.screen.get_height()))
            self.day_theme.stop()
            self.night_theme.play(-1)
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
        self.player.rect.x = 32
        self.player.rect.y = self.screen.get_height() - 64
        self.player.score = 0
        self.player.ammo = 0
        self.player.sprite_index = 0
        self.camera_offset = 0
        self.max_x = 0
        self.bg = pygame.transform.scale(pygame.image.load(join("assets", "background.png")), (self.screen.get_width(), self.screen.get_height()))
        self.game_over_sound.stop()
        self.game_clear_sound.stop()
        self.day_theme.play(-1)
        self.generate_map()





