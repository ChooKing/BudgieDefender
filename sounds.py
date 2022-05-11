import pygame.mixer

class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.small_explosion = pygame.mixer.Sound("./assets/small_explosion.wav")
