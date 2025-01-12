import pygame


class Sprites:
    def __init__(self, sheet):
        self.sheet = sheet

    def get_sprites(self, width, height, direction):
        images = []
        # Calculate the amount of sprites based on the width of the sprite sheet and the width provided
        image_count = self.sheet.get_width() // width
        for i in range(image_count):
            image = pygame.Surface((width, height)).convert_alpha()
            # Get each individual sprite
            image.blit(self.sheet, (0, 0), (i*width, 0, width, height))
            image.set_colorkey((0, 0, 0))
            images.append(image)

        # Either return the list or a dictionary with flipped sprites if the sprites have direction
        if direction:
            return {"left": self.flip_sprites(images), "right": images}

        return images

    def flip_sprites(self, sprites):
        original = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
        for sprite in original:
            sprite.set_colorkey((0, 0, 0))
        return original
