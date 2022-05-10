from collections.abc import Callable
from scaled_sprite import *


class Weapon(ABC):
    def __init__(self, owner: ScaledSprite):
        self.owner = owner
        self.speed = 0

    @abstractmethod
    def use(self, callback: Callable[[ScaledSprite], []]):
        pass
