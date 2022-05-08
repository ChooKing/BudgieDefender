from drawable import *


class ScaledSprite(Drawable):
    def __init__(self, ctx: pygame.surface,image: str, scale=1):
        super().__init__(ctx)
        self.image = pygame.image.load(image)
        if scale != 1:
            self.image = pygame.transform.smoothscale(self.image, (
                int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()

    def get_width(self) -> int:
        return self.rect.width

    def get_height(self) -> int:
        return self.rect.height

    def update(self):
        pass
