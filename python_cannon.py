from weapon import *
from snake import *
from scaled_sprite import *


class PythonCannon(Weapon):
    def __init__(self, owner: ScaledSprite, scale: float, speed: int):
        super().__init__(owner)
        self.snake_speed = speed
        self.scale = scale

    def use(self, callback: Callable[[Animation], []]):
        callback(Snake(self.owner.ctx, self.scale, self.owner.rect.x + int(self.owner.get_width()/2 - Snake.WIDTH * self.scale/2), self.owner.rect.y + (20 // self.scale), self.snake_speed))
        callback(Snake(self.owner.ctx, self.scale,
                       self.owner.rect.x + int(self.owner.get_width() / 2 - Snake.WIDTH * self.scale / 2) + (50 * self.scale),
                       self.owner.rect.y + (20 // self.scale), self.snake_speed))



