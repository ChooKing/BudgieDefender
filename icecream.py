from ammunition import *


class IceCream(Ammunition):
    WIDTH = 18  # Used for calculating center point before instantiating an icecream

    def __init__(self, x: int, y: int):
        super().__init__("./assets/icecream.bmp", 100, 0, -15, 0.25)
        self.rect.x = x
        self.rect.y = y


