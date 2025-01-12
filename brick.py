from block import Block


class Brick(Block):
    def __init__(self, x, y, daytime):
        super().__init__(x, y, daytime)

    def render(self, screen, camera_offset):
        screen.blit(self.sprites[1], (self.rect.x - camera_offset, self.rect.y))