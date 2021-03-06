from explodable import *
from mortal import *
from python_cannon import *
import random


class Airplane(ScaledSprite, Mortal, Explodable):
    WIDTH = 210
    ATTACK_RATE = 300 #Higher number results in less frequent snake launches

    def __init__(self, ctx: pygame.surface, scale: float, x: int, max_y: int, speed: int, register_ammo: Callable[[Animation], []], update_score: Callable[[int], []]):
        ScaledSprite.__init__(self, ctx, './assets/airplane.bmp', 0.5 * scale)
        Mortal.__init__(self, 6, False)
        Explodable.__init__(self, 0.5)
        self.rect.x = x
        self.max_y = max_y
        self.speed = speed
        self.exploding = False
        self.explosion_counter = 0
        self.weapon = PythonCannon(self, scale, speed + 1)
        self.register_ammo = register_ammo
        self.update_score = update_score
        self.scale_factor = scale


    def update(self):
        Mortal.update(self)
        if self.dead:
            self.update_score(5)
            self.kill()

        else:
            self.rect.y += self.speed
            if self.rect.y + self.rect.height > self.max_y:
                self.kill()

            if not random.randint(0, Airplane.ATTACK_RATE):
                self.weapon.use(self.register_ammo)

            if self.exploding:
                self.explosion_counter += 1


