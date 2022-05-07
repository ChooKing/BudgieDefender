from animation import *
from mortal import *


class Snake(Animation, Mortal):
    WIDTH = 100
    SPEED = 4

    def __init__(self, ctx: pygame.surface, x, y):
        Animation.__init__(self, ctx, './assets/python.bmp', 200, 2, 0.25, 4)
        Mortal.__init__(self, 4, False)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += Snake.SPEED
        Animation.update(self)
        Mortal.update(self)
        if self.dead:
            self.kill()
