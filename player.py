from enum import Enum
from beak import *


class Direction(Enum):
    LEFT = -1
    STILL = 0
    RIGHT = 1


class Player(Drawable):
    def __init__(self, image: str, scale: float, speed: int):
        super().__init__(image, scale)
        self.score = 0
        self.__direction = Direction.STILL
        self.speed = speed
        self.weapon = Beak(self)
        self.attacking = False

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction: Direction):
        self.__direction = direction

    def move(self, max_x: int, max_y: int):
        """max_x and max_y specify the extents for movement"""
        if self.direction == Direction.LEFT:
            if self.x - self.speed > 0:
                self.x -= self.speed
            else:
                self.x = 0
        elif self.direction == Direction.RIGHT:
            if self.x + self.speed + self.get_width() < max_x:
                self.x += self.speed
            else:
                self.x = max_x - self.get_width()


    def update(self):
        pass