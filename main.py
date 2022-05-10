import pygame.sprite
from player import *
from airplane import *
from explosion import *


class Game:
    BG_COLOR = (10, 20, 127)
    FRAME_RATE = 20
    STATUS_HEIGHT = 100

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Budgie Defender")
        pygame.key.set_repeat(1, 10)
        self.level = 1
        self.score = 0
        self.lives = 4
        self.font = pygame.font.Font('./assets/Goldman-Bold.ttf', 50)
        self.game_title = self.font.render("BUDGIE DEFENDER", True, (0, 255, 0))
        self.clock = pygame.time.Clock()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h - 100
        self.surface_width = self.screen_width
        self.surface_height = self.screen_height - Game.STATUS_HEIGHT
        self.main_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen = pygame.Surface((self.surface_width, self.surface_height))
        self.screen.fill(Game.BG_COLOR)
        self.stats_surface = pygame.Surface((self.screen_width, Game.STATUS_HEIGHT))

        self.sprites = pygame.sprite.Group()  #Used only to batch update but not draw
        self.snakes = pygame.sprite.Group()
        self.icecreams = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.player = Player(self.screen, "./assets/budgie.bmp", 0.25, 1, self.add_icecream, self.new_life)
        self.player.set_limits(self.surface_width, self.surface_height)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)), int(self.surface_height - self.player.get_height()))
        self.sprites.add(self.player)

        self.main_surface.blit(pygame.transform.scale(self.screen, (self.surface_width, self.surface_height)), (0, 0))
        pygame.display.flip()

        self.new_plane_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_plane_event, 300)
        self.plane_req_count = 0

    def add_plane(self):
        self.add_drawable(Airplane(self.screen, random.randint(self.player.get_width(), self.surface_width-self.player.get_width()), self.screen_height, self.add_snake, self.increment_score), self.planes)

    def add_icecream(self, drawable: ScaledSprite):
        self.sprites.add(drawable)
        self.icecreams.add(drawable)

    def add_snake(self, drawable: Animation):
        self.add_drawable(drawable, self.snakes)

    def add_drawable(self, drawable: Drawable, group: pygame.sprite.Group):
        self.sprites.add(drawable)
        group.add(drawable)

    def explode_planes(self, colliders):
        for (icecream, planes) in colliders.items():
            self.add_drawable(Explosion(self.screen, icecream.rect.x, icecream.rect.y), self.explosions)
            icecream.kill()
            for plane in planes:
                plane.dying = True

    def increment_score(self, amount: int):
        self.score += amount
        self.level = (self.score // 50) + 1

    def new_life(self):
        self.player.kill()
        self.lives -= 1
        self.planes.empty()
        self.snakes.empty()
        self.icecreams.empty()
        self.sprites.empty()
        self.player = Player(self.screen, "./assets/budgie.bmp", 0.25, 1, self.add_icecream, self.new_life)
        self.player.set_limits(self.surface_width, self.surface_height)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)),
                                 int(self.surface_height - self.player.get_height()))
        self.sprites.add(self.player)

    def draw_status(self):
        self.stats_surface.fill((0, 0, 0))
        self.stats_surface.blit(self.game_title, (20, 25))
        level_text = self.font.render(f"LEVEL: {self.level}", True, (0, 255, 0))
        self.stats_surface.blit(level_text, (750, 25))
        score_text = self.font.render(f"SCORE: {self.score}", True, (0, 255, 0))
        self.stats_surface.blit(score_text, (self.surface_width - score_text.get_width() - 20, 25))
        life_text = self.font.render(f"LIVES: {self.lives}", True, (0, 255, 0))
        self.stats_surface.blit(life_text, (self.surface_width - score_text.get_width() - life_text.get_width() - 40, 25))

    def update(self):
        self.screen.fill(Game.BG_COLOR)
        self.sprites.update()
        # Draw groups in separate batches to guarantee stacking order without performance penalty of OrderedUpdates
        self.snakes.draw(self.screen)
        self.planes.draw(self.screen)
        self.explosions.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.icecreams.draw(self.screen)

        if pygame.sprite.spritecollideany(self.player, self.snakes):
            self.player.dying = True

        colliders = pygame.sprite.groupcollide(self.icecreams, self.planes, False, False)
        if colliders:
            self.explode_planes(colliders)
        dead_snakes = pygame.sprite.groupcollide(self.icecreams, self.snakes, True, True)
        if dead_snakes:
            self.increment_score(1)

        self.main_surface.blit(pygame.transform.smoothscale(self.screen, (self.surface_width, self.surface_height)), (0, 0))

        self.draw_status()
        self.main_surface.blit(self.stats_surface, (0, self.surface_height))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        self.player.speedX -= 1
                    if keys[pygame.K_RIGHT]:
                        self.player.speedX += 1
                    if keys[pygame.K_SPACE]:
                        self.player.attacking = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.speedX = 0
                    if event.key == pygame.K_SPACE:
                        self.player.attacking = False

                elif event.type == self.new_plane_event:
                    if not self.player.dying:
                        self.plane_req_count += 1
                        if self.level > 11 or self.plane_req_count > (11 - self.level):
                            self.add_plane()
                            self.plane_req_count = 0

            self.update()
            pygame.display.update()
            self.clock.tick(Game.FRAME_RATE)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
