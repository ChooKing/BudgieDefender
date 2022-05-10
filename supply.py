from animation import *


class Supply(Animation):
    def __init__(self, ctx: pygame.surface, x: int, max_y: int):
        super().__init__(ctx, './assets/bigicecream.bmp', 146, 3, 1, 3)
        self.rect.x = x
        self.max_y = max_y
        self.ctx = ctx


    def update(self) -> None:
        super().update()
        self.rect.y += 5
        if self.rect.y > self.max_y:
            self.kill()
