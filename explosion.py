from animation import *
from mortal import *


class Explosion(Animation):
    def __init__(self, x, y):
        Animation.__init__(self, './assets/explosion.bmp', 200, 4, 0.5)
        Mortal.__init__(self, 4, True)
        self.rect.x = x - 50
        self.rect.y = y - 50
    def update(self):
        Animation.update(self)
        Mortal.update(self)
        if self.dead:
            self.kill()
