from collections.abc import Callable
from drawable import *


class Weapon(ABC):
    def __init__(self, owner: Drawable):
        self.ammunition = []
        self.owner = owner
        self.speed = 0

    @abstractmethod
    def use(self, callback: Callable[[Drawable], []]):
        pass
