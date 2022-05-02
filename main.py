import random

import pygame.sprite
from random import Random

from player import *
from icecream import *
from airplane import *
from typing import List


class Game:
    BG_COLOR = (10, 20, 127)
    FRAME_RATE = 20

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(1, 10)
        self.clock = pygame.time.Clock()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h - 100
        self.surface_width = 1920
        self.surface_height = 1080

        self.main_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen = pygame.Surface((self.surface_width, self.surface_height))
        self.screen.fill(Game.BG_COLOR)

        self.player = Player("./assets/budgie.bmp", 0.25, 1)
        self.player.set_limits(self.surface_width, self.surface_height)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)), int(self.surface_height - self.player.get_height()))


        self.drawables = pygame.sprite.Group()
        self.drawables.add(self.player)

        self.icecreams = pygame.sprite.Group()

        self.main_surface.blit(pygame.transform.scale(self.screen, (self.screen_width, self.screen_height)), (0, 0))
        self.frame = 0
        pygame.display.flip()

        self.new_plane_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_plane_event, 2500)
        self.planes = pygame.sprite.Group()



    def add_icecream(self, drawable: Drawable):
        self.drawables.add(drawable)
        self.icecreams.add(drawable)

    def explode_planes(self, colliders):

        for (icecream, planes) in colliders.items():

            icecream.kill()
            for plane in planes:
                plane.kill()


    def update(self):
        self.screen.fill(Game.BG_COLOR)

        self.drawables.update()
        self.drawables.draw(self.screen)


        if self.player.attacking:
            if self.frame % self.player.weapon.speed == 0:
                self.player.weapon.use(self.add_icecream)

        colliders = pygame.sprite.groupcollide(self.icecreams, self.planes, False, False)
        if colliders:
            self.explode_planes(colliders)

        self.main_surface.blit(pygame.transform.smoothscale(self.screen, (self.screen_width, self.screen_height)), (0, 0))

    def addplane(self):
        newplane = Airplane(random.randint(self.player.get_width(), self.surface_width-self.player.get_width()), self.screen_height)

        self.drawables.add(newplane)
        self.planes.add(newplane)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.speedX -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.player.speedX += 1
                    elif event.key == pygame.K_SPACE:
                        self.player.attacking = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.speedX = 0

                    if event.key == pygame.K_SPACE:
                        self.player.attacking = False
                elif event.type == self.new_plane_event:
                    self.addplane()

            self.update()
            pygame.display.update()
            self.clock.tick(Game.FRAME_RATE)
            self.frame += 1
            if self.frame > Game.FRAME_RATE:
                self.frame = 0


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
