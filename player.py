from beak import *


class Player(ScaledSprite):
    def __init__(self, ctx: pygame.surface, image: str, scale: float, speedfactor: int, on_use_weapon: Callable[[ScaledSprite],[]]):
        super().__init__(ctx, image, scale)
        self.max_y = 0
        self.max_x = 0
        self.score = 0
        self.speedX = 0
        self.speedY = 0
        self.speedfactor = speedfactor
        self.weapon = Beak(ctx, self)
        self.attacking = False
        self.on_use_weapon = on_use_weapon

    def set_limits(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y

    def update(self):
        if self.attacking:
            self.weapon.use(self.on_use_weapon)

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
