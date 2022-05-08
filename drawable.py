import pygame
from abc import ABC, abstractmethod


class Drawable(pygame.sprite.Sprite, ABC):
    def __init__(self, ctx: pygame.surface):
        super().__init__()
        self.ctx = ctx

    @abstractmethod
    def update(self):
        pass

    