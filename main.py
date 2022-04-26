import pygame.sprite

from player import *
from icecream import *
from typing import List


class Game:
    BG_COLOR = (10, 20, 127)
    FRAME_RATE = 20

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h - 100
        self.surface_width = 1920
        self.surface_height = 1080

        self.main_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen = pygame.Surface((self.surface_width, self.surface_height))
        self.screen.fill(Game.BG_COLOR)

        self.player = Player("./assets/budgie.bmp", 0.25, 30)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)), int(self.surface_height - self.player.get_height()))
        self.player.show()

        self.drawables = pygame.sprite.Group()
        self.drawables.add(self.player)

        self.main_surface.blit(pygame.transform.scale(self.screen, (self.screen_width, self.screen_height)), (0, 0))
        self.frame = 0
        pygame.display.flip()

    def add_drawable(self, drawable: Drawable):
        drawable.show()
        self.drawables.add(drawable)

    def update(self):
        if self.player.direction != Direction.STILL:
            self.player.move(self.surface_width, self.surface_height)

        self.screen.fill(Game.BG_COLOR)

        self.drawables.update()
        self.drawables.draw(self.screen)


        if self.player.attacking:
            if self.frame % self.player.weapon.speed == 0:
                self.player.weapon.use(self.add_drawable)

        self.main_surface.blit(pygame.transform.smoothscale(self.screen, (self.screen_width, self.screen_height)), (0, 0))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = Direction.RIGHT
                    elif event.key == pygame.K_SPACE:
                        self.player.attacking = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.direction = Direction.STILL

                    if event.key == pygame.K_SPACE:
                        self.player.attacking = False

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
