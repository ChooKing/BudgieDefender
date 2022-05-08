from scaled_sprite import *


class Ammunition(ScaledSprite):
    def __init__(self, ctx: pygame.surface, image: str, damage: int, speed_x: int, speed_y: int, scale=1):
        super().__init__(ctx, image, scale)
        self.damage = damage  # Number of health points subtracted upon impact
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.scale = scale  # Image scaling factor

    def update(self):
        """Propels ammunition one step forward per frame"""
        self.rect.x += self.speed_x
        if self.get_height() - self.speed_y > 0:
            self.rect.y += self.speed_y
        else:
            self.kill()


