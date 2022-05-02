from enum import Enum
from beak import *





class Player(Drawable):
    def __init__(self, image: str, scale: float, speedfactor: int):
        super().__init__(image, scale)
        self.max_y = 0
        self.max_x = 0
        self.score = 0
        self.speedX = 0
        self.speedY = 0
        self.speedfactor = speedfactor
        self.weapon = Beak(self)
        self.attacking = False

    def set_limits(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y

    def update(self):
        if self.speedX < 0:
            if self.rect.x + self.speedX * self.speedfactor > 0:
                self.rect.x += self.speedX * self.speedfactor
            else:
                self.rect.x = 0
        elif self.speedX > 0:
            if self.rect.x + self.speedX * self.speedfactor + self.get_width() < self.max_x:
                self.rect.x += self.speedX * self.speedfactor
            else:
                self.rect.x = self.max_x - self.get_width()
