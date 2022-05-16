import pygame.sprite
from player import *
from airplane import *
from explosion import *
from supply import *
from sounds import *
from enum import Enum


def in_rect(x: int, y: int, r: pygame.Rect):
    return r.x <= x <= r.x + r.width and r.y <= y <= r.y + r.height


class GameState(Enum):
    INTRO = 0
    HELP = 1
    PLAY = 2
    PAUSE = 3
    QUIT = 4
    OVER = 5


class Game:
    BG_COLOR = (10, 20, 127)
    FRAME_RATE = 20
    STATUS_HEIGHT = 100
    SUPPLY_SIZE = 50  # Quantity of ammo added by a big icecream

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Budgie Defender")
        pygame.key.set_repeat(150, 10)
        self.state = GameState.PLAY
        self.sounds = Sounds()
        self.level = 1
        self.score = 0
        self.lives = 4
        self.ammo = Game.SUPPLY_SIZE
        self.targets = 0  # Count targets to determine fair timing for resupply
        self.clock = pygame.time.Clock()
        self.scale_factor = 1 if pygame.display.Info().current_w / pygame.display.Info().current_h > 1.8 else 0.5
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h - 100
        self.surface_width = self.screen_width
        self.main_surface = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)


        Game.STATUS_HEIGHT = 100 * self.scale_factor
        self.surface_height = self.screen_height - Game.STATUS_HEIGHT
        self.screen = pygame.Surface((self.surface_width, self.surface_height))
        self.screen.fill(Game.BG_COLOR)
        self.stats_surface = pygame.Surface((self.screen_width, Game.STATUS_HEIGHT))
        self.font = pygame.font.Font('./assets/Goldman-Bold.ttf', int(50 * self.scale_factor))
        self.bigfont = pygame.font.Font('./assets/Goldman-Bold.ttf', int(150 * self.scale_factor))
        self.game_title = self.font.render("BUDGIE DEFENDER", True, (0, 255, 0))
        self.game_over = self.bigfont.render("GAME OVER", True, (255, 0, 0))
        self.play_again = self.font.render("PLAY AGAIN", True, (0, 255, 0))
        self.play_again_rect = pygame.Rect(self.main_surface.get_rect().centerx - self.play_again.get_width() // 2,
                                           self.main_surface.get_rect().centery - self.play_again.get_height() // 2
                                           - Game.STATUS_HEIGHT + 95,
                                           self.play_again.get_width(), self.play_again.get_height())
        self.exit = self.font.render("EXIT", True, (0, 255, 0))
        self.exit_rect = pygame.Rect(self.main_surface.get_rect().centerx - self.exit.get_width() // 2,
                                           self.main_surface.get_rect().centery - self.exit.get_height() // 2
                                           - Game.STATUS_HEIGHT + 170,
                                           self.exit.get_width(), self.exit.get_height())
        self.quit_prompt = self.bigfont.render("QUIT GAME?", True, (255, 0, 0))
        self.quit_text = self.font.render("QUIT", True, (0, 255, 0))
        self.continue_text = self.font.render("CONTINUE", True, (0, 255, 0))
        self.quit_text_rect = pygame.Rect(self.main_surface.get_rect().centerx - 35 -
                                          ((self.quit_text.get_width() + self.continue_text.get_width()) // 2),
                                           self.main_surface.get_rect().centery - self.quit_text.get_height() // 2
                                           - Game.STATUS_HEIGHT + 95,
                                           self.quit_text.get_width(), self.quit_text.get_height())
        self.continue_text_rect = pygame.Rect(self.main_surface.get_rect().centerx + 35 +
                                              ((self.quit_text.get_width() + self.continue_text.get_width()) // 2) -
                                              self.continue_text.get_width(),
                                           self.main_surface.get_rect().centery - self.quit_text.get_height() // 2
                                           - Game.STATUS_HEIGHT + 95,
                                           self.continue_text.get_width(), self.continue_text.get_height())
        self.background = pygame.image.load("./assets/background.bmp").convert(self.screen)
        self.background = pygame.transform.smoothscale(self.background, (self.screen_width, self.screen_height))
        self.sprites = pygame.sprite.Group()  # Used only to batch update but not draw
        self.snakes = pygame.sprite.Group()
        self.icecreams = pygame.sprite.Group()
        self.planes = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.supplies = pygame.sprite.Group()
        self.exploded = pygame.sprite.Group()  # Record exploded items to avoid double exploding same item

        self.nonexplosions = pygame.sprite.Group()

        self.player = Player(self.screen, "./assets/budgie.bmp", 0.25 * self.scale_factor, 1, self.add_icecream, self.new_life)
        self.player.set_limits(self.surface_width, self.surface_height)
        self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)),
                                 int(self.surface_height - self.player.get_height()))
        self.sprites.add(self.player)

        self.main_surface.blit(self.screen, (0, 0))
        pygame.display.flip()

        self.new_plane_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_plane_event, 300)
        self.plane_req_count = 0

    def rescale(self, width: int, height: int):
        self.screen_width = width
        self.screen_height = height - (100 * self.scale_factor)
        self.surface_width = width
        self.surface_height = height - Game.STATUS_HEIGHT
        self.screen = pygame.Surface((self.surface_width, self.surface_height))
        self.player.rect.y = self.surface_height - self.player.get_height()
        self.player.set_limits(self.surface_width, self.surface_height)


    def add_plane(self):
        self.add_drawable(
            Airplane(self.screen, self.scale_factor, random.randint(self.player.get_width(), self.surface_width - self.player.get_width()),
                     self.screen_height, self.level * 2, self.add_snake, self.increment_score), self.planes)
        self.targets += 1


    def add_supplies(self):
        self.add_drawable(
            Supply(self.screen, self.scale_factor, random.randint(self.player.get_width(), self.surface_width - self.player.get_width()),
                   self.screen_height), self.supplies)

    def add_icecream(self, drawable: ScaledSprite):
        self.sprites.add(drawable)
        self.icecreams.add(drawable)
        self.ammo -= 1
        self.sounds.shoot.play()

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
            self.add_drawable(Explosion(self.screen, x, y, exploder.explosion_size * self.scale_factor), self.explosions)
            if isinstance(exploder, Mortal):
                exploder.dying = True
                if isinstance(exploder, Airplane):
                    self.sounds.small_explosion.play()
            elif isinstance(exploder, Supply):
                exploder.kill()
                self.sounds.big_explosion.play()

    def increment_score(self, amount: int):
        self.score += amount
        self.level = (self.score // 100) + 1

    def new_life(self):
        self.player.kill()
        self.lives -= 1
        if self.lives > 0:
            self.planes.empty()
            self.snakes.empty()
            self.icecreams.empty()
            self.supplies.empty()
            self.explosions.empty()
            self.sprites.empty()

            self.player = Player(self.screen, "./assets/budgie.bmp", 0.25, 1, self.add_icecream, self.new_life)
            self.player.set_limits(self.surface_width, self.surface_height)
            self.player.rect.move_ip(int((self.surface_width / 2) - (self.player.get_width() / 2)),
                                     int(self.surface_height - self.player.get_height()))
            self.sprites.add(self.player)
        else:
            self.state = GameState.OVER

    def new_game(self):
        self.lives = 5  # new_life() decrements life by one
        self.score = 0
        self.level = 1
        self.ammo = Game.SUPPLY_SIZE
        self.targets = 0
        self.new_life()
        self.state = GameState.PLAY

    def draw_status(self):
        self.stats_surface.fill((0, 0, 0))
        self.stats_surface.blit(self.game_title, (20, int(25 * self.scale_factor)))
        level_text = self.font.render(f"LEVEL: {self.level}", True, (0, 255, 0))
        self.stats_surface.blit(level_text, (750, int(25 * self.scale_factor)))
        score_text = self.font.render(f"SCORE: {self.score}", True, (0, 255, 0))
        self.stats_surface.blit(score_text, (self.surface_width - score_text.get_width() - 20, int(25 * self.scale_factor)))
        life_text = self.font.render(f"LIVES: {self.lives}", True, (0, 255, 0))
        self.stats_surface.blit(life_text,
                                (self.surface_width - score_text.get_width() - life_text.get_width() - 40, int(25 * self.scale_factor)))
        ammo_text = self.font.render(f"AMMO: {self.ammo}", True, (0, 255, 0))
        self.stats_surface.blit(ammo_text, (
            self.surface_width - score_text.get_width() - life_text.get_width() - ammo_text.get_width() - 60, int(25 * self.scale_factor)))

    def update(self):
        if self.state == GameState.PLAY:
            self.screen.blit(self.background, (0, 0))
            self.sprites.update()
            # Draw groups in separate batches to guarantee stacking order without performance penalty of OrderedUpdates
            if self.targets > Game.SUPPLY_SIZE // 2:
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
                self.add_drawable(Explosion(self.screen, killer_plane.rect.centerx, killer_plane.rect.centery, 1),
                                  self.explosions)
                killer_plane.kill()

            colliders = pygame.sprite.groupcollide(self.icecreams, self.planes, False, False)
            if colliders:
                self.explode_planes(colliders)
            dead_snakes = pygame.sprite.groupcollide(self.icecreams, self.snakes, True, True)
            if dead_snakes:
                self.increment_score(1)
            new_ammo = pygame.sprite.spritecollideany(self.player, self.supplies)
            if new_ammo:
                self.add_supplies()
                self.sounds.take_supplies.play()
                self.ammo += Game.SUPPLY_SIZE
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

            self.main_surface.blit(self.screen, (0, 0))

            self.draw_status()
            self.main_surface.blit(self.stats_surface, (0, self.surface_height))
        elif self.state == GameState.PAUSE:
            pass
        elif self.state == GameState.QUIT:
            self.main_surface.blit(self.quit_prompt, (
                self.main_surface.get_rect().centerx - self.quit_prompt.get_width() // 2,
                self.main_surface.get_rect().centery - self.quit_prompt.get_height() // 2 - Game.STATUS_HEIGHT))
            self.main_surface.blit(self.quit_text, self.quit_text_rect)
            self.main_surface.blit(self.continue_text, self.continue_text_rect)
        elif self.state == GameState.OVER:
            self.main_surface.blit(self.game_over, (
                self.main_surface.get_rect().centerx - self.game_over.get_width() // 2,
                self.main_surface.get_rect().centery - self.game_over.get_height() // 2 - Game.STATUS_HEIGHT))
            self.main_surface.blit(self.play_again, self.play_again_rect)
            self.main_surface.blit(self.exit, self.exit_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.rescale(event.w, event.h)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.state == GameState.PLAY:
                            self.state = GameState.PAUSE
                            pygame.key.set_repeat(2000, 2000)
                        else:
                            self.state = GameState.PLAY
                            pygame.key.set_repeat(150, 10)
                        pygame.event.clear(eventtype=[pygame.KEYDOWN, pygame.KEYUP])
                    elif event.key == pygame.K_q:
                        self.state = GameState.QUIT
                    else:
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

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.state == GameState.OVER:
                        if in_rect(x, y, self.play_again_rect):
                            self.new_game()
                        elif in_rect(x, y, self.exit_rect):
                            pygame.quit()
                            quit()
                    elif self.state == GameState.QUIT:
                        if in_rect(x, y, self.quit_text_rect):
                            pygame.quit()
                            quit()
                        elif in_rect(x, y, self.continue_text_rect):
                            self.state = GameState.PLAY

                elif event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    if self.state == GameState.OVER:
                        if in_rect(x, y, self.play_again_rect) or in_rect(x, y, self.exit_rect):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    elif self.state == GameState.QUIT:
                        if in_rect(x, y, self.quit_text_rect) or in_rect(x, y, self.continue_text_rect):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
