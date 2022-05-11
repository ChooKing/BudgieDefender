from animation import *
from mortal import *


class Explosion(Animation, Mortal):
    def __init__(self, ctx: pygame.surface, x, y, scale):
        Animation.__init__(self, ctx, './assets/explosion.bmp', 400, 5, scale, 3)
        Mortal.__init__(self, 15, True)
        self.rect.centerx = x
        self.rect.centery = y
        self.ctx = ctx

    def update(self):
        Animation.update(self)
        Mortal.update(self)
        if self.dead:
            self.kill()
