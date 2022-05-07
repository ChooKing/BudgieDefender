from animation import *
from mortal import *


class Explosion(Animation, Mortal):
    def __init__(self, ctx: pygame.surface, x, y):
        Animation.__init__(self, ctx, './assets/explosion.bmp', 200, 4, 1, 2)
        Mortal.__init__(self, 4, True)
        self.rect.x = x - 100
        self.rect.y = y - 100
        self.ctx = ctx

    def update(self):
        Animation.update(self)
        Mortal.update(self)
        if self.dead:
            self.kill()
