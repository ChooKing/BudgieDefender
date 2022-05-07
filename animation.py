from drawable import *


class Animation(pygame.sprite.Sprite):
    def __init__(self, ctx: pygame.surface, image: str, width: int, count: int, scale: float, delay: int):
        pygame.sprite.Sprite.__init__(self)
        image_source = pygame.image.load(image)
        self.ctx = ctx
        if scale != 1:
            image_source = pygame.transform.smoothscale(image_source, (
                int(image_source.get_width() * scale), int(image_source.get_height() * scale)))
        height = image_source.get_height()
        self.images = []
        for i in range(count):
            self.images.append(image_source.subsurface(pygame.Rect(i * width * scale, 0, width * scale, height)))
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.delay = delay  # Number of game frames that mus elapse before advancing to next animation frame
        self.delay_count = 0

    def update(self) -> None:
        self.delay_count += 1
        if self.delay_count > self.delay:
            self.delay_count = 0
            self.frame += 1
            if self.frame > len(self.images) - 1:
                self.frame = 0
            self.image = self.images[self.frame]
