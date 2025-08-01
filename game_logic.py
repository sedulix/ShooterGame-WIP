import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLOR, GAME_CAPTION
from rocket import Rocket
from enemy import Skull
from ship import Ship


class Game:
    def __init__(self):
        pygame.display.set_caption(GAME_CAPTION)
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen_fill_color = SCREEN_COLOR
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_font = pygame.font.Font(None, 40)
        self.game_score = 0

        self.ship = Ship()
        self.skull = Skull()
        self.rocket = Rocket(self.ship)

        self.game_is_running = True


    def run(self):
        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.handle_key_events(event)

            self.update_game_state()
            self.draw_screen()

        self.show_game_over()


    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.ship.move_left()

            if event.key == pygame.K_RIGHT:
                self.ship.move_right()

            if event.key == pygame.K_UP:
                self.ship.move_up()

            if event.key == pygame.K_DOWN:
                self.ship.move_down()

            if event.key == pygame.K_SPACE:
                self.rocket.fire()

        if event.type == pygame.KEYUP:
            self.ship.stop_moving(event.key)


    def update_game_state(self):
        self.ship.update_position()
        self.skull.update_position()
        self.rocket.update_position()

        if self.rocket.is_out_of_screen():
            self.rocket.reset()

        if self.rocket.is_collision(self.skull):
            self.rocket.reset()
            self.skull.reset()
            self.game_score += 5000

        if self.skull.is_reached_ship(self.ship):
            self.game_is_running = False


    def draw_screen(self):
        self.screen.fill(SCREEN_COLOR)
        self.screen.blit(self.ship.image, (self.ship.x, self.ship.y))
        self.screen.blit(self.skull.image, (self.skull.x, self.skull.y))
        if self.rocket.was_fired:
            self.screen.blit(self.rocket.image, (self.rocket.x, self.rocket.y))
        self.show_game_score()
        pygame.display.update()


    def show_game_score(self):
        dev_score_text = self.game_font.render(f"Dev's highest score is: 190000", True, 'black')
        game_score_text = self.game_font.render(f"Your score is: {self.game_score}", True, "black")
        self.screen.blit(dev_score_text, (20, 20))
        self.screen.blit(game_score_text, (20, 60))


    def show_game_over(self):
        game_over_text = self.game_font.render("GAME OVER", True, 'black')
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.wait(3000)

