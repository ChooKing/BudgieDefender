from drawable import *
from mortal import *
from python_cannon import *
import random


class Airplane(Drawable, Mortal):
    WIDTH = 210
    ATTACK_RATE = 120
    SPEED = 2

    def __init__(self, ctx: pygame.surface, x: int, max_y: int, register_ammo: Callable[[Animation], []]):
        Drawable.__init__(self, ctx, './assets/airplane.bmp', 0.5)
        Mortal.__init__(self, 6, False)
        self.rect.x = x
        self.max_y = max_y
        self.exploding = False
        self.explosion_counter = 0
        self.weapon = PythonCannon(self)
        self.register_ammo = register_ammo


    def update(self):
        Mortal.update(self)
        if self.dead:
            self.kill()
        self.rect.y += Airplane.SPEED
        if self.rect.y + self.rect.height > self.max_y:
            self.kill()

        if not random.randint(0, Airplane.ATTACK_RATE):
            self.weapon.use(self.register_ammo)

        if self.exploding:
            self.explosion_counter += 1
            