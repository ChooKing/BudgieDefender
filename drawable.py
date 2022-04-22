import pygame
from abc import ABC, abstractmethod


class Drawable(pygame.sprite.Sprite, ABC):
    def __init__(self, image: str, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        if scale != 1:
            self.image = pygame.transform.smoothscale(self.image, (
                int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def get_width(self) -> int:
        return self.rect.width

    def get_height(self) -> int:
        return self.rect.height

    @abstractmethod
    def update(self):
        pass

    def draw(self, destination: pygame.Surface):
        if self.visible:
            destination.blit(self.image, (self.x, self.y))

