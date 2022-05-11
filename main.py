import pygame.sprite
from player import *
from airplane import *
from explosion import *
from supply import *


class Game:
    BG_COLOR = (10, 20, 127)
    FRAME_RATE = 20
    STATUS_HEIGHT = 100
    SUPPLY_SIZE = 50  # Quantity of ammo added by a big icecream

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Budgie Defender")
        pygame.key.set_repeat(1, 10)
        self.level = 1
        self.score = 0
        self.lives = 4
        self.ammo = 25
        self.targets = 0  # Count targets to determine fair timing for resupply
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

        self.background = pygame.image.load("./assets/background.bmp").convert(self.screen)
        self.background = pygame.transform.smoothscale(self.background, (self.screen_width, self.screen_height))
        self.sprites = pygame.sprite.Group()  #Used only to batch update but not draw
        self.snakes = pygame.sprite.Group()
        self.icecreams = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.supplies = pygame.sprite.Group()
        self.exploded = pygame.sprite.Group()  # Record exploded items to avoid double exploding same item

        self.nonexplosions = pygame.sprite.Group()

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
        self.targets += 1

    def add_supplies(self):
        self.add_drawable(
            Supply(self.screen, random.randint(self.player.get_width(), self.surface_width - self.player.get_width()),
                     self.screen_height), self.supplies)

    def add_icecream(self, drawable: ScaledSprite):
        self.sprites.add(drawable)
        self.icecreams.add(drawable)
        self.ammo -= 1

    def add_snake(self, drawable: Animation):
        self.add_drawable(drawable, self.snakes)
        self.targets += 1

    def add_drawable(self, drawable: Drawable, group: pygame.sprite.Group):
        self.sprites.add(drawable)
        if not isinstance(drawable, Explosion):
            self.nonexplosions.add(drawable)
        group.add(drawable)

    def explode_planes(self, colliders):
        for (icecream, planes) in colliders.items():
            for plane in planes:
                self.explode(plane, icecream.rect.centerx, icecream.rect.y)
            icecream.kill()

    def explode(self, exploder: pygame.sprite.Sprite, x: int, y: int):
        self.exploded.add(exploder)
        if isinstance(exploder, Explodable):
            self.add_drawable(Explosion(self.screen, x, y, exploder.explosion_size), self.explosions)
            if isinstance(exploder, Mortal):
                exploder.dying = True
            elif isinstance(exploder, Supply):
                exploder.kill()



    def increment_score(self, amount: int):
        self.score += amount
        self.level = (self.score // 50) + 1

    def new_life(self):
        self.player.kill()
        self.lives -= 1
        self.planes.empty()
        self.snakes.empty()
        self.icecreams.empty()
        self.supplies.empty()
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
        ammo_text = self.font.render(f"AMMO: {self.ammo}", True, (0, 255, 0))
        self.stats_surface.blit(ammo_text, (self.surface_width - score_text.get_width() - life_text.get_width() - ammo_text.get_width() - 60, 25))

    def update(self):
        self.screen.blit(self.background, (0 , 0))
        self.sprites.update()
        # Draw groups in separate batches to guarantee stacking order without performance penalty of OrderedUpdates
        if self.targets > Game.SUPPLY_SIZE // 4:
            self.targets = 0
            self.add_supplies()
        self.snakes.draw(self.screen)
        self.planes.draw(self.screen)
        self.supplies.draw(self.screen)
        self.explosions.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.icecreams.draw(self.screen)


        killer_snake = pygame.sprite.spritecollideany(self.player, self.snakes)
        if killer_snake:
            self.player.dying = True
            killer_snake.kill()  # Remove snake that killed the budgie without awarding a point
        killer_plane = pygame.sprite.spritecollideany(self.player, self.planes)
        if killer_plane:
            self.player.dying = True
            self.add_drawable(Explosion(self.screen, killer_plane.rect.centerx, killer_plane.rect.centery, 1), self.explosions)
            killer_plane.kill()

        colliders = pygame.sprite.groupcollide(self.icecreams, self.planes, False, False)
        if colliders:
            self.explode_planes(colliders)
        dead_snakes = pygame.sprite.groupcollide(self.icecreams, self.snakes, True, True)
        if dead_snakes:
            self.increment_score(1)
        new_ammo = pygame.sprite.spritecollideany(self.player, self.supplies)
        if new_ammo:
            self.ammo += 50
            new_ammo.kill()
        destroyed_supplies = pygame.sprite.groupcollide(self.supplies, self.icecreams, False, True)
        if destroyed_supplies:
            for supply in destroyed_supplies:
                self.explode(supply, supply.rect.centerx, supply.rect.centery)
                supply.kill()
        cascade_exploders = pygame.sprite.groupcollide(self.nonexplosions, self.explosions, False, False)
        if cascade_exploders:
            for exploder in cascade_exploders:
                if isinstance(exploder, Snake):
                    self.score += 1
                    exploder.kill()
                elif not self.exploded.has(exploder):
                    self.exploded.add(exploder)
                    self.explode(exploder, exploder.rect.centerx, exploder.rect.centery)
                    if isinstance(exploder, Airplane):
                        self.score += 5

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

                if self.ammo < 1:
                    self.player.attacking = False
            self.update()
            pygame.display.update()
            self.clock.tick(Game.FRAME_RATE)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
