from weapon import *
from icecream import *
from drawable import *


class Beak(Weapon):
    def __init__(self, owner: Drawable):
        super().__init__(owner)
        self.speed = 3  # Higher number is slower firing rate

    def use(self, callback: Callable[[Drawable], []]):
        callback(IceCream(self.owner.rect.x + int(self.owner.get_width()/2 - IceCream.WIDTH/2), self.owner.rect.y))

