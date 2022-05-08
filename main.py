import random

import pygame.sprite
from random import Random

from player import *
from icecream import *
from airplane import *
from typing import List

from explosion import *

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



        self.player = Player(self.screen, "./assets/budgie.bmp", 0.25, 1)
        self.player.set_limits(self.surface_width, self.surface_height)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)), int(self.surface_height - self.player.get_height()))


        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)

        self.snakes = pygame.sprite.Group()

        self.icecreams = pygame.sprite.Group()

        self.main_surface.blit(pygame.transform.scale(self.screen, (self.screen_width, self.screen_height)), (0, 0))
        self.frame = 0
        pygame.display.flip()

        self.new_plane_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_plane_event, 2500)
        self.planes = pygame.sprite.Group()




    def add_icecream(self, drawable: ScaledSprite):
        self.sprites.add(drawable)
        self.icecreams.add(drawable)

    def add_snake(self, drawable: Animation):

        self.snakes.add(drawable)

    def explode_planes(self, colliders):

        for (icecream, planes) in colliders.items():
            self.sprites.add(Explosion(self.screen, icecream.rect.x, icecream.rect.y))
            icecream.kill()
            for plane in planes:
                plane.dying = True


    def update(self):
        self.screen.fill(Game.BG_COLOR)
        self.snakes.update()
        self.snakes.draw(self.screen)

        self.sprites.update()
        self.sprites.draw(self.screen)



        if self.player.attacking:
            if self.frame % self.player.weapon.speed == 0:
                self.player.weapon.use(self.add_icecream)

        colliders = pygame.sprite.groupcollide(self.icecreams, self.planes, False, False)
        if colliders:
            self.explode_planes(colliders)
        dead_snakes = pygame.sprite.groupcollide(self.icecreams, self.snakes, True, True)
        if dead_snakes:
            pass  #Increase score

        self.main_surface.blit(pygame.transform.smoothscale(self.screen, (self.screen_width, self.screen_height)), (0, 0))

    def addplane(self):
        newplane = Airplane(self.screen, random.randint(self.player.get_width(), self.surface_width-self.player.get_width()), self.screen_height, self.add_snake)

        self.sprites.add(newplane)
        self.planes.add(newplane)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.speedX -= 2
                    elif event.key == pygame.K_RIGHT:
                        self.player.speedX += 2
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
