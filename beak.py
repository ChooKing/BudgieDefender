from weapon import *
from icecream import *
from scaled_sprite import *


class Beak(Weapon):
    def __init__(self, ctx: pygame.surface, owner: ScaledSprite):
        super().__init__(owner)
        self.speed = 2  # Higher number is slower firing rate
        self.ctx = ctx
        self.use_count = 0

    def use(self, callback: Callable[[ScaledSprite], []]):
        self.use_count += 1
        if self.use_count > self.speed:
            self.use_count = 0
            callback(IceCream(self.ctx, self.owner.rect.x + int(self.owner.get_width()/2 - IceCream.WIDTH/2), self.owner.rect.y))

