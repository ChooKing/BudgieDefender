from collections.abc import Callable
from drawable import *


class Weapon(ABC):
    def __init__(self, owner: Drawable, ammo_qty):
        self.ammo_qty = ammo_qty  # -1 for infinite
        self.owner = owner
        self.speed = 0

    @abstractmethod
    def use(self, callback: Callable[[Drawable], []]):
        pass
