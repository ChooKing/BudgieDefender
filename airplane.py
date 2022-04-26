from drawable import *


class Airplane(Drawable):
    WIDTH = 210
    def __init__(self, x, max_y):
        super().__init__('./assets/airplane.bmp', 0.5)
        self.rect.x = x
        self.max_y = max_y
        self.exploding = False
        self.explosion_counter = 0

    def update(self):
        self.rect.y += 5
        if self.rect.y + self.rect.height > self.max_y:
            self.kill()

        if self.exploding:
            self.explosion_counter += 1
            