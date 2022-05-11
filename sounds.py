import pygame.mixer


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.small_explosion = pygame.mixer.Sound("./assets/small_explosion.wav")
        self.big_explosion = pygame.mixer.Sound("./assets/big_explosion.wav")
        self.take_supplies = pygame.mixer.Sound("./assets/take_supplies.wav")
        self.shoot = pygame.mixer.Sound("./assets/shoot.wav")
