from drawable import *


class Animation(pygame.sprite.Sprite):
    def __init__(self, image: str, width: int, count: int, scale=1):
        pygame.sprite.Sprite.__init__(self)
        image_source = pygame.image.load(image)
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

    def update(self) -> None:
        self.frame += 1
        if self.frame > len(self.images) - 1:
            self.frame = 0
        self.image = self.images[self.frame]