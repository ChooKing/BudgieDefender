from weapon import *
from snake import *
from drawable import *


class PythonCannon(Weapon):
    def __init__(self, owner: Drawable):
        super().__init__(owner, -1)
        self.speed = 3  # Higher number is slower firing rate

    def use(self, callback: Callable[[Animation], []]):
        callback(Snake(self.owner.ctx, self.owner.rect.x + int(self.owner.get_width()/2 - Snake.WIDTH/2), self.owner.rect.y + 20))
        callback(Snake(self.owner.ctx, self.owner.rect.x + int(self.owner.get_width() / 2 - Snake.WIDTH / 2) + 50,
                       self.owner.rect.y + 20))

