from weapon import *
from icecream import *
from scaled_sprite import *


class Beak(Weapon):
    def __init__(self, ctx: pygame.surface, owner: ScaledSprite):
        super().__init__(owner, -1)
        self.speed = 3  # Higher number is slower firing rate
        self.ctx = ctx

    def use(self, callback: Callable[[ScaledSprite], []]):
        callback(IceCream(self.ctx, self.owner.rect.x + int(self.owner.get_width()/2 - IceCream.WIDTH/2), self.owner.rect.y))

