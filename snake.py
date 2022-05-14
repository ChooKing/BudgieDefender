from animation import *


class Snake(Animation):
    WIDTH = 100

    def __init__(self, ctx: pygame.surface, x: int, y: int, speed: int):
        super().__init__(ctx, './assets/python.bmp', 200, 2, 0.25, 4)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        super().update()



