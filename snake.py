from animation import *


class Snake(Animation):
    WIDTH = 100
    SPEED = 4

    def __init__(self, ctx: pygame.surface, x, y):
        super().__init__(ctx, './assets/python.bmp', 200, 2, 0.25, 4)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += Snake.SPEED
        super().update()

