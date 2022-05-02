from drawable import *
from mortal import *


class Airplane(Drawable, Mortal):
    WIDTH = 210
    def __init__(self, x, max_y):
        Drawable.__init__(self, './assets/airplane.bmp', 0.5)
        Mortal.__init__(self, 4, False)
        self.rect.x = x
        self.max_y = max_y
        self.exploding = False
        self.explosion_counter = 0

    def update(self):
        Mortal.update(self)
        if self.dead:
            self.kill()
        self.rect.y += 5
        if self.rect.y + self.rect.height > self.max_y:
            self.kill()

        if self.exploding:
            self.explosion_counter += 1
            