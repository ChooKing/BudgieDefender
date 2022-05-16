from explodable import *
from animation import *


class Supply(Animation, Explodable):
    def __init__(self, ctx: pygame.surface, scale: float, x: int, max_y: int):
        Animation.__init__(self, ctx, './assets/bigicecream.bmp', 146, 3, scale, 3)
        Explodable.__init__(self, 1)
        self.rect.x = x
        self.max_y = max_y
        self.ctx = ctx


    def update(self) -> None:
        super().update()
        self.rect.y += 5
        if self.rect.y > self.max_y:
            self.kill()
